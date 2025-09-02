from fastapi import APIRouter, Depends, HTTPException, Request, Header
from sqlalchemy.orm import Session
from sqlalchemy import select
from config.database import get_db
from config.security import create_jwt, hash_password, verify_password
from schemas.tenant import TenantCreate, TenantSettingsOut
from schemas.auth import LoginIn, TokenOut
from models.tenant import Tenant, TenantSettings
from models.user import User
from middleware.tenant import set_current_tenant

router = APIRouter(prefix="/tenant", tags=["tenant"])

def _get_tenant_by_key(db: Session, key: str | None) -> Tenant | None:
    if not key:
        return None
    return db.execute(select(Tenant).where(Tenant.subdomain == key)).scalar_one_or_none()

@router.post("/login", response_model=TokenOut)
def tenant_login(payload: LoginIn, request: Request, db: Session = Depends(get_db)):
    tenant_key = request.headers.get("x-tenant") or getattr(request.state, "tenant_key", None)
    tenant = _get_tenant_by_key(db, tenant_key)
    if not tenant:
        raise HTTPException(status_code=400, detail="Tenant inválido (use subdomínio ou header X-Tenant)")
    set_current_tenant(db, tenant.id)

    user = db.execute(select(User).where(User.email == payload.email, User.tenant_id == tenant.id)).scalar_one_or_none()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = create_jwt(sub=user.id, tenant_id=tenant.id, role=user.role)
    return TokenOut(access_token=token)

@router.get("/settings", response_model=TenantSettingsOut)
def tenant_settings(request: Request, db: Session = Depends(get_db)):
    tenant_key = request.headers.get("x-tenant") or getattr(request.state, "tenant_key", None)
    tenant = _get_tenant_by_key(db, tenant_key)
    if not tenant:
        return TenantSettingsOut()
    set_current_tenant(db, tenant.id)
    s = db.execute(select(TenantSettings).where(TenantSettings.tenant_id == tenant.id)).scalar_one_or_none()
    if not s:
        return TenantSettingsOut()
    return TenantSettingsOut(logo_url=s.logo_url, theme_primary=s.theme_primary, theme_secondary=s.theme_secondary)

@router.post("/admin/create")
def admin_create_tenant(payload: TenantCreate, admin_token: str = Header(None, alias="Admin-Token"), db: Session = Depends(get_db)):
    from ..config.settings import settings
    if admin_token != settings.ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Forbidden")
    exists = db.execute(select(Tenant).where(Tenant.subdomain == payload.subdomain)).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=409, detail="Subdomínio já existe")

    t = Tenant(name=payload.name, subdomain=payload.subdomain, plan="basic")
    db.add(t); db.flush()

    ts = TenantSettings(tenant_id=t.id)
    db.add(ts)

    user = User(
        tenant_id=t.id,
        name=payload.admin_name,
        email=payload.admin_email,
        password_hash=hash_password(payload.admin_password),
        role="admin"
    )
    db.add(user)
    db.commit()

    return {"ok": True, "tenant_id": t.id, "subdomain": t.subdomain, "admin_email": user.email}

