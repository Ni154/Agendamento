# backend/models/appointment.py
from datetime import datetime
from backend import db

class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, nullable=False)
    service_id = db.Column(db.Integer, nullable=False)

    date = db.Column(db.Date, nullable=False, index=True)
    time = db.Column(db.Time, nullable=False, index=True)

    status = db.Column(db.String(20), nullable=False, default="PENDENTE")
    notes = db.Column(db.Text, nullable=False, default="")

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.Index("ix_appointments_date_time", "date", "time"),
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "client_id": self.client_id,
            "service_id": self.service_id,
            "date": self.date.isoformat() if self.date else None,
            "time": self.time.strftime("%H:%M") if self.time else None,
            "status": self.status,
            "notes": self.notes or "",
        }

    def __repr__(self) -> str:
        return f"<Appointment id={{self.id}} date={{self.date}} time={{self.time}} status={{self.status}}>"
