from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config.database import engine, Base

# Import das rotas criadas
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

from dotenv import load_dotenv
import os

# Carregar variáveis ambiente
load_dotenv()

app = FastAPI(title="Studio Depilação API")

# Configuração CORS - ajuste os origins para o domínio do frontend em produção
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Criar todas as tabelas no banco, baseadas nos modelos
Base.metadata.create_all(bind=engine)

# Incluir rotas
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

