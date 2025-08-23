from flask import Blueprint, request, jsonify
from backend import db

# Modelo (tenta o arquivo real e, se existir, aceita shim *_model.py)
try:
    from backend.models.servico import Servico
except Exception:
    from backend.models.servico_model import Servico  # opcional, se você tiver um shim

serv_bp = Blueprint("servicos", __name__)  # <-- ESTE é o nome que o __init__.py importa

def _to_dict(s):
    if hasattr(s, "to_dict"):
        return s.to_dict()
    # fallback caso o modelo não tenha to_dict
    return {c.name: getattr(s, c.name) for c in s.__table__.columns}

@serv_bp.get("/")
def listar():
    itens = Servico.query.order_by(Servico.nome.asc()).all()
    return jsonify({"ok": True, "items": [_to_dict(s) for s in itens]})

@serv_bp.get("/<int:sid>")
def obter(sid):
    s = Servico.query.get(sid)
    if not s:
        return jsonify({"ok": False, "error": "Serviço não encontrado."}), 404
    return jsonify({"ok": True, "item": _to_dict(s)})

@serv_bp.post("/")
def criar():
    data = request.get_json(silent=True) or {}
    nome = (data.get("nome") or "").strip()
    if not nome:
        return jsonify({"ok": False, "error": "Informe o nome do serviço."}), 400

    s = Servico(
        nome=nome,
        categoria=(data.get("categoria") or "").strip(),
        descricao=(data.get("descricao") or "").strip(),
        preco=float(data.get("preco") or 0),
        duracao_min=int(data.get("duracao_min") or 0),
    )
    db.session.add(s)
    db.session.commit()
    return jsonify({"ok": True, "item": _to_dict(s)}), 201

@serv_bp.put("/<int:sid>")
def atualizar(sid):
    s = Servico.query.get(sid)
    if not s:
        return jsonify({"ok": False, "error": "Serviço não encontrado."}), 404
    data = request.get_json(silent=True) or {}
    for campo in ("nome", "categoria", "descricao", "preco", "duracao_min"):
        if campo in data and data[campo] is not None:
            val = data[campo]
            if campo == "preco":
                val = float(val or 0)
            if campo == "duracao_min":
                val = int(val or 0)
            setattr(s, campo, val)
    db.session.commit()
    return jsonify({"ok": True, "item": _to_dict(s)})

@serv_bp.delete("/<int:sid>")
def excluir(sid):
    s = Servico.query.get(sid)
    if not s:
        return jsonify({"ok": False, "error": "Serviço não encontrado."}), 404
    db.session.delete(s)
    db.session.commit()
    return jsonify({"ok": True})
