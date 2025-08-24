# backend/config.py
import os
from dotenv import load_dotenv

# Carrega variáveis do ambiente (em produção no Railway você define em Variables;
# em dev/local pode usar um .env)
load_dotenv()

class Config:
    # --- App / Segurança ---
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

    # --- Banco de Dados ---
    # Lê URL do ambiente; normaliza prefixo e SSL quando necessário
    database_url = os.getenv("DATABASE_URL")

    if database_url and database_url.startswith("postgres://"):
        # Normaliza URL antiga para SQLAlchemy
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    # Railway (host *.proxy.rlwy.net) geralmente exige SSL
    if database_url and "proxy.rlwy.net" in database_url and "sslmode=" not in database_url:
        sep = "&" if "?" in database_url else "?"
        database_url = f"{database_url}{sep}sslmode=require"

    SQLALCHEMY_DATABASE_URI = database_url or "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- E-mail (opcional) ---
    RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
    MAIL_FROM = os.getenv("MAIL_FROM", "noreply@example.com")

    # --- URLs auxiliares ---
    APP_BASE_URL = os.getenv("APP_BASE_URL", "http://127.0.0.1:5000")

    # --- Prefixos para rotas ---
    API_PREFIX = os.getenv("API_PREFIX", "/api")
    AUTH_PREFIX = os.getenv("AUTH_PREFIX", "/api/auth")

    # --- CORS ---
    # Permite configurar múltiplas origens separadas por vírgula
    _cors_origins_raw = os.getenv("CORS_ALLOW_ORIGINS", "*")
    CORS_ALLOW_ORIGINS = [o.strip() for o in _cors_origins_raw.split(",")] if _cors_origins_raw else ["*"]
    CORS_ALLOW_CREDENTIALS = os.getenv("CORS_ALLOW_CREDENTIALS", "true").strip().lower() == "true"
