import uuid
from datetime import datetime, timedelta
from backend import db

class PasswordResetToken(db.Model):
    __tablename__ = "password_reset_tokens"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, index=True)
    token = db.Column(db.String(64), unique=True, nullable=False, index=True)
    expires_at = db.Column(db.DateTime, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<PasswordResetToken user_id={self.user_id} exp={self.expires_at.isoformat()}>"

    @staticmethod
    def new_token():
        return uuid.uuid4().hex

    @classmethod
    def expires_in(cls, hours: int = 1):
        return datetime.utcnow() + timedelta(hours=hours)
