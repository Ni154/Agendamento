# backend/routes/auth_routes.py
import os
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash

from backend import db
from backend.models.user_model import User
from backend.models.reset_token_model import PasswordResetToken

import resend

auth_bp = Blueprint("auth", __name__)

# ---------- Helpers ----------
# --- RESEND helpers ---
def ensure_resend_config():
    # pega da config ou do ambiente
    if not resend.api_key:
        key = current_app.config.get("RESEND_API_KEY") or os.getenv("RESEND_API_KEY", "")
        resend.api_key = key

def send_email_resend(to: str, subject: str, html: str) -> dict | None:
    """
    Tenta enviar via Resend. Loga sucesso/erro e devolve o dict de resposta.
    Em dev, usa 'onboarding@resend.dev' se MAIL_FROM não estiver setado.
    """
    ensure_resend_config()
    mail_from = current_app.config.get("MAIL_FROM") or "onboarding@resend.dev"

    if not resend.api_key:
        current_app.logger.error("[RESEND] RESEND_API_KEY ausente.")
        return None

    try:
        resp = resend.Emails.send({
            "from": mail_from,
            "to": [to],
            "subject": subject,
            "html": html
        })
        # resp tipicamente: {'id': 'email_...'}
        current_app.logger.info(f"[RESEND] enviado para {to} id={resp.get('id')}")
        return resp
    except Exception as e:
        current_app.logger.error(f"[RESEND] falha: {e}")
        return None

# ---------- Rotas ----------
@auth_bp.route("/register", methods=["POST", "OPTIONS"])
def register():
    if request.method == "OPTIONS":
        return ("", 204)

    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not name or not email or not password:
        return jsonify({"ok": False, "error": "Preencha nome, e-mail e senha."}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"ok": False, "error": "E-mail já cadastrado."}), 409

    user = User(name=name, email=email, password_hash=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()

    # e-mail de boas-vindas (best-effort)
    send_email_resend(
        to=email,
        subject="Bem-vinda(o) ao Studio Priscila Santos",
        html=f"<p>Olá, {name}! Sua conta foi criada com sucesso.</p>"
    )

    return jsonify({"ok": True, "user": user.to_dict()}), 201


@auth_bp.route("/login", methods=["POST", "OPTIONS"])
def login():
    if request.method == "OPTIONS":
        return ("", 204)

    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"ok": False, "error": "Informe e-mail e senha."}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"ok": False, "error": "Credenciais inválidas."}), 401

    return jsonify({"ok": True, "user": user.to_dict()}), 200


@auth_bp.route("/recover", methods=["POST", "OPTIONS"])
def recover():
    if request.method == "OPTIONS":
        return ("", 204)

    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    if not email:
        return jsonify({"ok": False, "error": "Informe o e-mail."}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        # não revela existência
        return jsonify({"ok": True}), 200

    token = PasswordResetToken.new_token()
    rec = PasswordResetToken(
        user_id=user.id,
        token=token,
        expires_at=PasswordResetToken.expires_in(1)
    )
    db.session.add(rec)
    db.session.commit()

    # monta link usando host atual se APP_BASE_URL não estiver setada
    # monta link usando host atual se APP_BASE_URL não estiver setada
    base = current_app.config.get("APP_BASE_URL") or request.host_url.rstrip("/")
    link = f"{base}/reset.html?token={token}"

    send_email_resend(
        to=email,
        subject="Redefinição de senha",
        html=(
            f"<h3>Redefinição de senha</h3>"
            f"<p>Olá, {user.name}.</p>"
            f"<p>Clique no link abaixo para redefinir sua senha (expira em 1 hora):</p>"
            f'<p><a href="{link}">{link}</a></p>'
        )
    )

    # <<< DEV-HELP: em desenvolvimento, já retorna o link no JSON >>>
    # depois de montar 'link' e chamar send_email_resend(...)
    if current_app.config.get("FLASK_ENV") == "development":
        current_app.logger.info(f"[DEV] Link de reset: {link}")
        return jsonify({"ok": True, "link": link}), 200
    return jsonify({"ok": True}), 200


@auth_bp.route("/reset", methods=["POST", "OPTIONS"])
def reset():
    if request.method == "OPTIONS":
        return ("", 204)

    data = request.get_json(silent=True) or {}
    token = (data.get("token") or "").strip()
    new_password = data.get("password") or ""

    if not token or not new_password:
        return jsonify({"ok": False, "error": "Token e nova senha são obrigatórios."}), 400

    rec = PasswordResetToken.query.filter_by(token=token).first()
    if not rec:
        return jsonify({"ok": False, "error": "Token inválido."}), 400

    if rec.expires_at < datetime.utcnow():
        db.session.delete(rec)
        db.session.commit()
        return jsonify({"ok": False, "error": "Token expirado."}), 400

    user = User.query.get(rec.user_id)
    if not user:
        db.session.delete(rec)
        db.session.commit()
        return jsonify({"ok": False, "error": "Usuário não encontrado."}), 404

    user.password_hash = generate_password_hash(new_password)
    db.session.delete(rec)
    db.session.commit()

    return jsonify({"ok": True}), 200

@auth_bp.post("/_debug/send_test")
def send_test_email():
    """
    Envia um e-mail de teste via Resend para o endereço informado (JSON: { "to": "..." }).
    Útil em desenvolvimento para diagnosticar.
    """
    data = request.get_json(silent=True) or {}
    to = (data.get("to") or "").strip()
    if not to:
        return jsonify({"ok": False, "error": "Informe 'to'"}), 400

    resp = send_email_resend(
        to=to,
        subject="Teste de envio (Resend) — Studio Priscila Santos",
        html="<p>Se você recebeu este e-mail, o Resend está funcionando ✅</p>"
    )
    if resp and resp.get("id"):
        return jsonify({"ok": True, "id": resp["id"]}), 200
    return jsonify({"ok": False, "error": "Falha ao enviar (veja logs no servidor)"}), 500
