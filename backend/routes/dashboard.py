from flask import Blueprint, jsonify
from datetime import datetime, date, timedelta
from sqlalchemy import func
from backend import db
from backend.models.cliente import Cliente
from backend.models.produto import Produto
from backend.models.sale import Sale
from backend.models.despesa import Despesa
from backend.models.appointment import Appointment

dash_bp = Blueprint("dashboard", __name__)

@dash_bp.get("/")
def kpis():
    today = date.today()
    tomorrow = today + timedelta(days=1)

    clientes_total = db.session.query(func.count(Cliente.id)).scalar() or 0
    estoque_total = db.session.query(func.coalesce(func.sum(Produto.estoque),0)).scalar() or 0
    faturamento_hoje = (db.session.query(func.coalesce(func.sum(Sale.total),0))
                        .filter(Sale.created_at >= datetime.combine(today, datetime.min.time()),
                                Sale.created_at < datetime.combine(tomorrow, datetime.min.time()),
                                Sale.status=="completed").scalar() or 0)
    despesas_hoje = (db.session.query(func.coalesce(func.sum(Despesa.total),0))
                     .filter(Despesa.data == today).scalar() or 0)
    agendamentos_hoje = (db.session.query(func.count(Appointment.id))
                         .filter(Appointment.start_at >= datetime.combine(today, datetime.min.time()),
                                 Appointment.start_at < datetime.combine(tomorrow, datetime.min.time())).scalar() or 0)

    return jsonify({
        "ok": True,
        "clientes_total": int(clientes_total),
        "estoque_total": int(estoque_total),
        "faturamento_hoje": float(faturamento_hoje),
        "despesas_hoje": float(despesas_hoje),
        "resultado_hoje": float(faturamento_hoje - despesas_hoje),
        "agendamentos_hoje": int(agendamentos_hoje),
    })
