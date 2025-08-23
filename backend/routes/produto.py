from flask import Blueprint, request, jsonify
from backend import db
from ..models.produto import Produto

prod_bp = Blueprint("produtos", __name__)

@prod_bp.get("/")
def listar():
    qs = Produto.query.order_by(Produto.nome.asc()).all()
    return jsonify({"ok": True, "items": [p.to_dict() for p in qs]})

@prod_bp.post("/")
def criar():
    data = request.get_json() or {}
    p = Produto(
        nome=(data.get("nome") or "").strip(),
        sku=(data.get("sku") or "").strip(),
        categoria=(data.get("categoria") or "").strip(),
        unidade=(data.get("unidade") or "").strip(),
        preco_custo=float(data.get("preco_custo") or 0),
        preco_venda=float(data.get("preco_venda") or 0),
        estoque_qtd=float(data.get("estoque_qtd") or 0),
    )
    if not p.nome:
        return jsonify({"ok": False, "error": "Informe o nome."}), 400
    db.session.add(p); db.session.commit()
    return jsonify({"ok": True, "item": p.to_dict()}), 201
