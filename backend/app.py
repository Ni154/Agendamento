# backend/app.py
import os, sys, traceback

# Garantir que a raiz do projeto (pasta que contém "backend/") está no PYTHONPATH
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    from backend import create_app
    from backend.config import Config
except Exception:
    print("\n[FALHA] import backend / Config")
    traceback.print_exc()
    raise

# Expor app para servidores WSGI (gunicorn)
app = create_app()

if __name__ == "__main__":
    host = os.getenv("FLASK_RUN_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_RUN_PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "1") == "1" or os.getenv("FLASK_ENV") == "development"

    try:
        uri = Config.SQLALCHEMY_DATABASE_URI
        engine_part = uri.split("://", 1)[0]
        engine, driver = (engine_part.split("+", 1) + [""])[:2]
        print(f"[DB] Usando: {uri}  (engine={engine}{'+'+driver if driver else ''})")
    except Exception:
        pass

    app.run(host=host, port=port, debug=debug)
