from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import select
from config.database import get_db
from config.security import decode_jwt
from models.user import User
from tenant import set_current_tenant

bearer = HTTPBearer(auto_error=False)

async def get_current_user(request: Request, credentials: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)):
    if credentials is None:
        raise HTTPException(status_code=401, detail="Missing token")
    try:
        data = decode_jwt(credentials.credentials)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    tenant_id = data.get("tenant_id")
    user_id = data.get("sub")
    if not tenant_id or not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    set_current_tenant(db, tenant_id)
    user = db.execute(select(User).where(User.id == user_id, User.tenant_id == tenant_id)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    request.state.tenant_id = tenant_id
    return user

