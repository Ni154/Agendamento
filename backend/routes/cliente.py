# backend/routes/cliente.py
from flask import Blueprint, request, jsonify
from backend import db
from ..models.cliente import Cliente  # modelo já corrigido

clientes_bp = Blueprint("clientes", __name__)  # <— ESTE NOME é o que o __init__.py importa

def _to_dict(c: Cliente):
    if hasattr(c, "to_dict"):
        return c.to_dict()
    return {col.name: getattr(c, col.name) for col in c.__table__.columns}

def _payload(data: dict, allow_update=False):
    cols = {c.name for c in Cliente.__table__.columns}
    cols.discard("id")
    if not allow_update:
        for k in ("criado_em", "atualizado_em", "created_at", "updated_at"):
            cols.discard(k)
    return {k: v for k, v in (data or {}).items() if k in cols}

@clientes_bp.get("/")
def listar():
    q = (request.args.get("q") or "").strip()
    limit = min(int(request.args.get("limit", 50)), 200)
    qry = Cliente.query
    if q:
        from sqlalchemy import or_
        tests = []
        for col in ("nome", "apelido", "email", "telefone", "whatsapp", "cpf"):
            if hasattr(Cliente, col):
                tests.append(getattr(Cliente, col).ilike(f"%{q}%"))
        if tests:
            qry = qry.filter(or_(*tests))
    itens = qry.order_by(Cliente.id.desc()).limit(limit).all()
    return jsonify({"ok": True, "items": [_to_dict(c) for c in itens]})

@clientes_bp.get("/<int:cid>")
def obter(cid):
    c = Cliente.query.get(cid)
    if not c:
        return jsonify({"ok": False, "error": "Cliente não encontrado."}), 404
    return jsonify({"ok": True, "item": _to_dict(c)})

@clientes_bp.post("/")
def criar():
    data = request.get_json(silent=True) or {}
    payload = _payload(data, allow_update=False)

    nome = (payload.get("nome") or "").strip()
    if not nome:
        return jsonify({"ok": False, "error": "Informe o nome do cliente."}), 400

    if "email" in payload and hasattr(Cliente, "email"):
        email = (payload.get("email") or "").strip().lower()
        if email:
            exists = Cliente.query.filter(Cliente.email == email).first()
            if exists:
                return jsonify({"ok": False, "error": "E-mail já cadastrado."}), 409
        payload["email"] = email

    c = Cliente(**payload)
    db.session.add(c)
    db.session.commit()
    return jsonify({"ok": True, "item": _to_dict(c)}), 201

@clientes_bp.put("/<int:cid>")
def atualizar(cid):
    c = Cliente.query.get(cid)
    if not c:
        return jsonify({"ok": False, "error": "Cliente não encontrado."}), 404

    data = request.get_json(silent=True) or {}
    payload = _payload(data, allow_update=True)

    if "email" in payload and hasattr(Cliente, "email"):
        novo_email = (payload.get("email") or "").strip().lower()
        if novo_email and novo_email != (getattr(c, "email", "") or ""):
            exists = Cliente.query.filter(Cliente.email == novo_email, Cliente.id != cid).first()
            if exists:
                return jsonify({"ok": False, "error": "E-mail já cadastrado para outro cliente."}), 409
        payload["email"] = novo_email

    for k, v in payload.items():
        setattr(c, k, v)
    db.session.commit()
    return jsonify({"ok": True, "item": _to_dict(c)})

@clientes_bp.delete("/<int:cid>")
def excluir(cid):
    c = Cliente.query.get(cid)
    if not c:
        return jsonify({"ok": False, "error": "Cliente não encontrado."}), 404
    db.session.delete(c)
    db.session.commit()
    return jsonify({"ok": True})
