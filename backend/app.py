# backend/app.py
import os
import traceback

try:
    # Quando o serviço tem Root Directory = backend/, o pacote atual é o próprio diretório.
    # Portanto, importamos direto de __init__ e config locais.
    from __init__ import create_app
    from config import Config
except Exception:
    print("\n[FALHA] import create_app / Config")
    traceback.print_exc()
    raise

# Expor app para servidores WSGI (gunicorn) e para execução direta
app = create_app()

if __name__ == "__main__":
    host = os.getenv("FLASK_RUN_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_RUN_PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "1") == "1" or os.getenv("FLASK_ENV") == "development"

    # Log amigável da conexão de banco (sem mostrar senha)
    try:
        uri = Config.SQLALCHEMY_DATABASE_URI
        engine_part = uri.split("://", 1)[0]
        engine, driver = (engine_part.split("+", 1) + [""])[:2]
        print(f"[DB] Usando: {uri}  (engine={engine}{'+'+driver if driver else ''})")
    except Exception:
        pass

    app.run(host=host, port=port, debug=debug)
