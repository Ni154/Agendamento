from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config.database import engine, Base
from dotenv import load_dotenv
import os

# --- Carregar variáveis de ambiente ---
load_dotenv()

print("\n🔹 Conectando ao banco de dados:")
print(f"Host: {os.getenv('POSTGRES_HOST')}")
print(f"Banco: {os.getenv('POSTGRES_DB')}")
print(f"Usuário: {os.getenv('POSTGRES_USER')}\n")

# --- Importar todos os models para registrar no metadata ---
from backend.models import (
    cliente_model,
    produto_model,
    servico_model,
    agendamento_model,
    venda_model,
    despesa_model
)

# --- Criar tabelas ---
Base.metadata.create_all(bind=engine)
print("✅ Tabelas criadas/verificadas com sucesso!\n")

# --- Inicializar FastAPI ---
app = FastAPI(title="Studio Depilação API")

# --- Configuração CORS ---
origins = [
    "https://agendamento-banco-de-dados.up.railway.app",  # backend
    "https://<seu-nome-no-streamlit>.streamlit.app",       # frontend
]

if os.getenv("ENV", "dev") == "dev":
    origins.extend([
        "http://localhost:8501",
        "http://127.0.0.1:8501"
    ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Importar rotas ---
from backend.routes.usuario_routes import router as usuario_router
from backend.routes.cliente_routes import router as cliente_router
from backend.routes.produto_routes import router as produto_router
from backend.routes.servico_routes import router as servico_router
from backend.routes.venda_routes import router as venda_router
from backend.routes.despesa_routes import router as despesa_router
from backend.routes.agendamento_routes import router as agendamento_router
from backend.routes.backup_routes import router as backup_router
from backend.routes.dashboard_routes import router as dashboard_router
from backend.routes.relatorio_routes import router as relatorio_router

# --- Adicionar rotas ---
app.include_router(usuario_router, prefix="/usuario", tags=["Usuário"])
app.include_router(cliente_router, prefix="/cliente", tags=["Cliente"])
app.include_router(produto_router, prefix="/produto", tags=["Produto"])
app.include_router(servico_router, prefix="/servico", tags=["Serviço"])
app.include_router(venda_router, prefix="/venda", tags=["Venda"])
app.include_router(despesa_router, prefix="/despesa", tags=["Despesa"])
app.include_router(agendamento_router, prefix="/agendamento", tags=["Agendamento"])
app.include_router(backup_router, prefix="/backup", tags=["Backup"])
app.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(relatorio_router, prefix="/relatorio", tags=["Relatório"])

@app.get("/")
def root():
    return {"message": "API Studio Depilação rodando"}
