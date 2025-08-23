from flask import Blueprint, request, jsonify
from backend import db
from ..models.venda import Venda, VendaItem
from ..models.produto import Produto
from ..models.servico import Servico


try:
    # se você tem o modelo de agendamento:
    from ..models.appointment_model import Appointment   # opcional
except Exception:
    Appointment = None

vendas_bp = Blueprint("vendas", __name__)

VALID_PG = {"dinheiro", "credito", "debito", "pix"}

def _to_decimal(x, default="0"):
    try:
        return Decimal(str(x))
    except Exception:
        return Decimal(default)

def _normalize_items(items):
    """
    Aceita itens em dois formatos e normaliza para:
    {produto_id, servico_id, descricao, qtd, preco_unit}
    Formato novo:  {produto_id, servico_id, qtd, preco_unit}
    Formato antigo:{kind|tipo, ref_id, nome?, unit_price, qtd}
    """
    norm = []
    for it in (items or []):
        pid = it.get("produto_id")
        sid = it.get("servico_id")
        desc = (it.get("descricao") or it.get("nome") or "").strip()
        qtd = it.get("qtd")
        pu  = it.get("preco_unit", it.get("unit_price"))

        # formato antigo: kind/ref_id
        if not pid and not sid and (it.get("kind") or it.get("tipo")) and it.get("ref_id"):
            kind = (it.get("kind") or it.get("tipo")).lower()
            if kind == "produto":
                pid = it.get("ref_id")
            elif kind == "servico":
                sid = it.get("ref_id")

        # saneamento
        try:
            pid = int(pid) if pid else None
        except Exception:
            pid = None
        try:
            sid = int(sid) if sid else None
        except Exception:
            sid = None

        try:
            qtd = float(qtd or 0)
        except Exception:
            qtd = 0.0

        pu_dec = _to_decimal(pu, "0")

        if (pid or sid) and qtd > 0 and pu_dec >= 0:
            norm.append({
                "produto_id": pid,
                "servico_id": sid,
                "descricao": desc,
                "qtd": qtd,
                "preco_unit": pu_dec
            })
    return norm

@vendas_bp.get("/")
def listar():
    qs = Venda.query.order_by(Venda.id.desc()).limit(200).all()
    return jsonify({"ok": True, "items": [v.to_dict() for v in qs]})

@vendas_bp.get("/<int:vid>")
def obter(vid):
    v = Venda.query.get(vid)
    if not v:
        return jsonify({"ok": False, "error": "Venda não encontrada."}), 404
    return jsonify({"ok": True, "item": v.to_dict()})

@vendas_bp.post("/")
def criar():
    data = request.get_json(silent=True) or {}

    forma = (data.get("forma_pagamento") or "").lower().strip()
    if forma not in VALID_PG:
        return jsonify({"ok": False, "error": "Forma de pagamento inválida. Use: dinheiro|credito|debito|pix."}), 400

    itens_norm = _normalize_items(data.get("itens") or data.get("items"))
    if not itens_norm:
        return jsonify({"ok": False, "error": "Inclua ao menos um item válido."}), 400

    v = Venda(
        cliente_id = data.get("cliente_id"),
        forma_pagamento = forma,
        observacoes = (data.get("observacoes") or data.get("notes") or "").strip(),
        total = 0.0
    )
    db.session.add(v)
    db.session.flush()

    total = Decimal("0")

    for it in itens_norm:
        pid = it["produto_id"]
        sid = it["servico_id"]
        desc = it["descricao"]
        qtd = float(it["qtd"])
        pu  = it["preco_unit"]              # Decimal
        linha_total = pu * Decimal(str(qtd))
        total += linha_total

        vi = VendaItem(
            venda_id=v.id,
            produto_id=pid,
            servico_id=sid,
            descricao=desc,
            qtd=qtd,
            preco_unit=float(pu),            # armazena como float no banco
            total=float(linha_total)
        )
        db.session.add(vi)

        # baixa estoque de produto
        if pid:
            p = Produto.query.get(pid)
            if not p:
                db.session.rollback()
                return jsonify({"ok": False, "error": f"Produto {pid} inexistente."}), 400
            # seu modelo usa estoque_qtd (não 'estoque')
            nova_qtd = (p.estoque_qtd or 0) - qtd
            p.estoque_qtd = nova_qtd if nova_qtd >= 0 else 0

    v.total = float(total)
    db.session.commit()

    # Se você quiser marcar agendamento como finalizado,
    # inclua appointment_id no payload e trate aqui (opcional),
    # só se existir modelo Appointment.
    # Exemplo:
    # if Appointment:
    #     ap_id = data.get("appointment_id")
    #     if ap_id:
    #         ap = Appointment.query.get(ap_id)
    #         if ap:
    #             ap.status = "FINALIZADO"
    #             db.session.commit()

    return jsonify({"ok": True, "item": v.to_dict()}), 201

@vendas_bp.post("/<int:vid>/cancelar")
def cancelar(vid):
    v = Venda.query.get(vid)
    if not v:
        return jsonify({"ok": False, "error": "Venda não encontrada."}), 404

    # Repor estoque dos produtos desta venda
    for it in v.itens:
        if it.produto_id:
            p = Produto.query.get(it.produto_id)
            if p:
                p.estoque_qtd = (p.estoque_qtd or 0) + (it.qtd or 0)

    # OBS: seu modelo Venda atual NÃO tem campo 'status/cancelada'.
    # Se quiser persistir estado de cancelamento, adicione coluna depois.
    db.session.commit()
    return jsonify({"ok": True})
