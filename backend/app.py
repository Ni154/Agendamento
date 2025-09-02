from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from .config.settings import settings
from .config.database import Base, engine, SessionLocal
from .middleware.tenant import TenantInjectorMiddleware
from .routes import (
    health,
    auth_routes,
    tenant_routes,
    cliente_routes,
    produto_routes,
    servico_routes,
    agendamento_routes,
    venda_routes,
    despesa_routes,
)

app = FastAPI(title="SaaS Multi-tenant", version="1.0.0")

def _install_cors(app: FastAPI):
    origins = settings.ALLOWED_ORIGINS
    allow_origins = []
    allow_origin_regex = None
    allow_credentials = True

    if "*" in origins:
        allow_origins = ["*"]
        allow_credentials = False
    else:
        literal = [o for o in origins if not o.lower().startswith("regex:")]
        regexes = [o[len("regex:"):] for o in origins if o.lower().startswith("regex:")]
        allow_origins = literal
        if regexes:
            allow_origin_regex = "|".join(f"(?:{r})" for r in regexes)
        else:
            allow_origin_regex = settings.ALLOWED_ORIGIN_REGEX_FALLBACK

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_origin_regex=allow_origin_regex,
        allow_credentials=allow_credentials,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

_install_cors(app)

app.add_middleware(TenantInjectorMiddleware)

app.include_router(health.router)
app.include_router(tenant_routes.router)
app.include_router(auth_routes.router)
app.include_router(cliente_routes.router)
app.include_router(produto_routes.router)
app.include_router(servico_routes.router)
app.include_router(agendamento_routes.router)
app.include_router(venda_routes.router)
app.include_router(despesa_routes.router)

def _bootstrap_db():
    if settings.DATABASE_URL.startswith("postgresql"):
        with SessionLocal() as db:
            db.execute(text("CREATE EXTENSION IF NOT EXISTS pgcrypto;"))
            db.commit()
    Base.metadata.create_all(bind=engine)

    if settings.DATABASE_URL.startswith("postgresql"):
        rls_tables = ["tenant_settings","users","clientes","produtos","servicos","agendamentos","vendas","despesas","reset_tokens"]
        with SessionLocal() as db:
            for t in rls_tables:
                db.execute(text(f"ALTER TABLE IF EXISTS {t} ENABLE ROW LEVEL SECURITY;"))
                db.execute(text(f"DROP POLICY IF EXISTS {t}_isolate ON {t};"))
                db.execute(text(f"""
                    CREATE POLICY {t}_isolate ON {t}
                    USING (tenant_id::text = current_setting('app.current_tenant', true))
                    WITH CHECK (tenant_id::text = current_setting('app.current_tenant', true));
                """))
            db.commit()

@app.on_event("startup")
def on_startup():
    _bootstrap_db()

@app.get("/")
def root():
    return {"ok": True, "service": "SaaS Multi-tenant API"}
