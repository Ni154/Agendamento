# backend/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config  # <- import local (sem "backend.")

db = SQLAlchemy()

def _try_import_bp(modpath: str, bpname: str):
    """Tenta importar um blueprint; retorna (bp, error_str)."""
    import importlib, traceback, io
    try:
        mod = importlib.import_module(modpath)
        bp = getattr(mod, bpname)
        return bp, None
    except Exception as e:
        buf = io.StringIO()
        traceback.print_exc(file=buf)
        return None, f"[IMPORT ERRO] {modpath}.{bpname}: {e.__class__.__name__}: {e}\n{buf.getvalue()}"

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    # Registra blueprints (sem prefixo 'backend.' pois o Root é 'backend/')
    routes_to_register = [
        ("routes.auth_routes", "auth_bp",        "/api/auth"),
        ("routes.cliente",     "clientes_bp",    "/api/clientes"),
        ("routes.produto",     "prod_bp",        "/api/produtos"),
        ("routes.servico",     "serv_bp",        "/api/servicos"),
        ("routes.despesas",    "desp_bp",        "/api/despesas"),
        ("routes.vendas",      "vendas_bp",      "/api/vendas"),
        ("routes.relatorios",  "rel_bp",         "/api/relatorios"),
        ("routes.appointments","appts_bp",       "/api/agendamentos"),
    ]

    for modpath, bpname, prefix in routes_to_register:
        bp, err = _try_import_bp(modpath, bpname)
        if bp:
            app.register_blueprint(bp, url_prefix=prefix)
        else:
            print(err or f"[WARN] Falha ao importar {modpath}.{bpname}")

    # Endpoints utilitários
    @app.get("/api/health")
    def health():
        return {"ok": True}

    @app.get("/api/debug/db")
    def debug_db():
        from sqlalchemy import text
        eng = db.engine
        url_safe = eng.url.render_as_string(hide_password=True)
        try:
            with eng.connect() as conn:
                conn.execute(text("SELECT 1"))
                status = "ok"
        except Exception as e:
            status = f"error: {e.__class__.__name__}: {e}"
        return {
            "ok": status == "ok",
            "status": status,
            "url": url_safe,
            "dialect": eng.dialect.name,
            "driver": getattr(eng.dialect, "driver", None),
        }

    with app.app_context():
        db.create_all()

    return app
