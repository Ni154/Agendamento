from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Carrega variáveis do .env (caso esteja rodando localmente)
load_dotenv()

# Pega a URL completa do banco direto do Railway
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL não encontrada nas variáveis de ambiente!")

# Cria o engine do SQLAlchemy
engine = create_engine(DATABASE_URL)

# Sessão padrão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()
