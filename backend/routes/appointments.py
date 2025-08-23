from datetime import date, time
from flask import Blueprint, request, jsonify
from backend import db
from ..models.appointment import Appointment

# Nome do blueprint deve bater com __init__.py
appts_bp = Blueprint("agendamentos", __name__)

@appts_bp.get("/")
def list_appointments():
    d = request.args.get("date")
    q = Appointment.query
    if d:
        try:
            q = q.filter(Appointment.date == date.fromisoformat(d))
        except Exception:
            return jsonify({"ok": False, "error": "Data inválida. Use YYYY-MM-DD"}), 400
    items = q.order_by(Appointment.date.asc(), Appointment.time.asc()).all()
    return jsonify({"ok": True, "items": [a.to_dict() for a in items]})

@appts_bp.post("/")
def create_appointment():
    data = request.get_json() or {}
    try:
        a = Appointment(
            client_id=int(data.get("client_id")),
            service_id=int(data.get("service_id")),
            date=date.fromisoformat(data.get("date")),
            time=time.fromisoformat(data.get("time")+":00") if len(data.get("time",""))==5 else time.fromisoformat(data.get("time")),
            status=(data.get("status") or "PENDENTE"),
            notes=(data.get("notes") or "").strip(),
        )
    except Exception as e:
        return jsonify({"ok": False, "error": f"Payload inválido: {e}"}), 400

    db.session.add(a)
    db.session.commit()
    return jsonify({"ok": True, "item": a.to_dict()}), 201

@appts_bp.put("/<int:aid>/status")
def update_status(aid):
    a = Appointment.query.get_or_404(aid)
    data = request.get_json() or {}
    new = (data.get("status") or "").upper()
    if new not in ("PENDENTE","EM_ANDAMENTO","FINALIZADO"):
        return jsonify({"ok": False, "error": "Status inválido."}), 400
    a.status = new
    db.session.commit()
    return jsonify({"ok": True, "item": a.to_dict()})
