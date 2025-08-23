# backend/routes/despesas.py
from datetime import date
from flask import Blueprint, request, jsonify
from backend import db

# >>> IMPORTS CORRETOS (sem *_model) <<<
from backend.models.despesa import Despesa
from backend.models.produto import Produto

desp_bp = Blueprint("despesas", __name__)

@desp_bp.post("/")
def criar():
    data = request.get_json(silent=True) or {}
    categoria = (data.get("categoria") or "").strip().lower()  # "revenda" | "uso"
    if categoria not in ("revenda", "uso"):
        return jsonify({"ok": False, "error": "Categoria deve ser 'revenda' ou 'uso'."}), 400

    d = Despesa(
        data = date.fromisoformat(data.get("data")) if data.get("data") else date.today(),
        fornecedor = (data.get("fornecedor") or "").strip(),
        categoria = categoria,
        observacoes = (data.get("observacoes") or "").strip(),
        total = 0.0
    )
    db.session.add(d)

    itens = data.get("itens") or []
    if not itens:
        return jsonify({"ok": False, "error": "Informe ao menos um item."}), 400

    total = 0.0
    for it in itens:
        qtd = float(it.get("qtd") or 0)
        custo = float(it.get("custo_unit") or it.get("custo") or 0)
        if qtd <= 0 or custo < 0:
            return jsonify({"ok": False, "error": "Item inválido (qtd/custo)."}), 400

        total += qtd * custo

        if categoria == "revenda":
            pid = it.get("produto_id")
            if not pid:
                return jsonify({"ok": False, "error": "produto_id é obrigatório para 'revenda'."}), 400
            p = Produto.query.get(pid)
            if not p:
                return jsonify({"ok": False, "error": f"Produto {pid} inexistente."}), 404

            old_qtd = float(p.estoque_qtd or 0.0)
            old_custo = float(p.preco_custo or 0.0)
            new_qtd = old_qtd + qtd
            new_total_custo = (old_qtd * old_custo) + (qtd * custo)

            p.estoque_qtd = new_qtd
            p.preco_custo = (new_total_custo / new_qtd) if new_qtd > 0 else custo

    d.total = total
    db.session.commit()
    return jsonify({"ok": True, "id": d.id, "total": d.total}), 201
