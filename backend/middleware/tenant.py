from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

def _get_subdomain(host: str) -> str | None:
    if not host:
        return None
    parts = host.split(":")[0].split(".")
    if len(parts) <= 2:
        return None
    return parts[0]

class TenantInjectorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        header_tenant = request.headers.get("x-tenant")
        host = request.headers.get("host", "")
        tenant_key = header_tenant or _get_subdomain(host)
        request.state.tenant_key = tenant_key  # None para rotas públicas
        return await call_next(request)

def set_current_tenant(db: Session, tenant_id: str):
    db.execute(text("SELECT set_config('app.current_tenant', :t, true)"), {"t": tenant_id})

