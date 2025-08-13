from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config.database import engine, Base
from dotenv import load_dotenv
import os

load_dotenv()

# IMPORTANTE: importar models para registrar no metadata
from backend.models import (
    Cliente, Produto, Servico, Agendamento, Venda, Despesa, Usuario
)

# Cria/verifica tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Studio Depilação API")

# Ajuste o domínio do seu Streamlit aqui
origins = [
    "https://agendamento-banco-de-dados.up.railway.app",   # backend
    "https://SEU-APP.streamlit.app",                       # frontend streamlit
    "http://localhost:8501",
    "http://127.0.0.1:8501",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
from backend.routes.cliente_routes import router as cliente_router
from backend.routes.produto_routes import router as produto_router
from backend.routes.servico_routes import router as servico_router
from backend.routes.agendamento_routes import router as agendamento_router
from backend.routes.venda_routes import router as venda_router
from backend.routes.despesa_routes import router as despesa_router

# Se usar a rota de login pronta acima:
from backend.routes.auth_routes import router as auth_router

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(cliente_router, prefix="/cliente", tags=["Cliente"])
app.include_router(produto_router, prefix="/produto", tags=["Produto"])
app.include_router(servico_router, prefix="/servico", tags=["Serviço"])
app.include_router(agendamento_router, prefix="/agendamento", tags=["Agendamento"])
app.include_router(venda_router, prefix="/venda", tags=["Venda"])
app.include_router(despesa_router, prefix="/despesa", tags=["Despesa"])

@app.get("/")
def root():
    return {"message": "API Studio Depilação rodando"}
