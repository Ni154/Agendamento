from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.hash import bcrypt
from .settings import settings

ALGO = "HS256"

def hash_password(pwd: str) -> str:
    return bcrypt.hash(pwd)

def verify_password(pwd: str, hashed: str) -> bool:
    return bcrypt.verify(pwd, hashed)

def create_jwt(sub: str, tenant_id: str, role: str, minutes: Optional[int] = None) -> str:
    exp_min = minutes or settings.JWT_EXPIRES_MIN
    payload = {
        "sub": sub,
        "tenant_id": tenant_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(minutes=exp_min)
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=ALGO)

def decode_jwt(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[ALGO])

