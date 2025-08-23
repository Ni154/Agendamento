# backend/routes/relatorios.py
from flask import Blueprint, request, jsonify
from datetime import datetime, date, timedelta
from sqlalchemy import func
from backend import db
from backend.models.sale import Sale
from backend.models.despesa import Despesa

rel_bp = Blueprint("relatorios", __name__)

@rel_bp.get("/resumo")
def resumo():
    di = request.args.get("data_inicio")
    df = request.args.get("data_fim")
    try:
        start = datetime.fromisoformat(di) if di else datetime.combine(date.today(), datetime.min.time())
        end   = datetime.fromisoformat(df) if df else datetime.combine(date.today()+timedelta(days=1), datetime.min.time())
    except Exception:
        return jsonify({"ok": False, "error": "datas inválidas (use ISO)."}), 400

    faturamento = (db.session.query(func.coalesce(func.sum(Sale.total), 0))
                   .filter(Sale.created_at >= start, Sale.created_at < end, Sale.status == "completed")
                   .scalar()) or 0
    despesas = (db.session.query(func.coalesce(func.sum(Despesa.total), 0))
                .filter(Despesa.data >= start.date(), Despesa.data < end.date())
                .scalar()) or 0

    return jsonify({
        "ok": True,
        "periodo": {"inicio": start.isoformat(), "fim": end.isoformat()},
        "faturamento": float(faturamento),
        "despesas": float(despesas),
        "resultado": float(faturamento - despesas),
    })

@rel_bp.get("/vendas")
def rel_vendas():
    di = request.args.get("data_inicio")
    df = request.args.get("data_fim")
    start = datetime.fromisoformat(di) if di else datetime.combine(date.today(), datetime.min.time())
    end   = datetime.fromisoformat(df) if df else datetime.combine(date.today()+timedelta(days=1), datetime.min.time())
    q = (Sale.query
         .filter(Sale.created_at >= start, Sale.created_at < end)
         .order_by(Sale.id.desc())
         .limit(500)
         .all())
    return jsonify([s.to_dict() for s in q])

@rel_bp.get("/despesas")
def rel_despesas():
    di = request.args.get("data_inicio")
    df = request.args.get("data_fim")
    start = date.fromisoformat(di) if di else date.today()
    end   = date.fromisoformat(df) if df else date.today()
    q = (Despesa.query
         .filter(Despesa.data >= start, Despesa.data <= end)
         .order_by(Despesa.id.desc())
         .limit(500)
         .all())
    out = []
    for d in q:
        out.append({
            "id": d.id,
            "data": d.data.isoformat(),
            "categoria": d.categoria.nome if d.categoria else None,
            "natureza": d.categoria.natureza if d.categoria else None,
            "fornecedor": d.fornecedor.nome if d.fornecedor else None,
            "total": float(d.total),
        })
    return jsonify(out)
