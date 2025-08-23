import bcrypt
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from backend.config import FLASK_SECRET

def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False

_serializer = URLSafeTimedSerializer(FLASK_SECRET)

def make_reset_token(user_id: str) -> str:
    return _serializer.dumps({"uid": user_id})

def parse_reset_token(token: str, max_age_seconds: int = 3600) -> str | None:
    try:
        data = _serializer.loads(token, max_age=max_age_seconds)
        return data.get("uid")
    except (BadSignature, SignatureExpired):
        return None
