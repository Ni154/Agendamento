from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Variáveis do Railway - você pode trocar para ler do .env se preferir
DB_USER = "postgres"
DB_PASSWORD = "IItWDGjcnNIDuCQlpGnKeiPhwmoaFhNh"
DB_HOST = "postgres.railway.internal"
DB_PORT = "5432"
DB_NAME = "railway"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependência para injetar session no FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
