from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import (
    cliente_routes,
    produto_routes,
    servico_routes,
    venda_routes,
    despesa_routes,
    agendamento_routes,
    usuario_routes,
    backup,
    dashboard,
    relatorio,
)

app = FastAPI(title="API Studio Depilação")

# Configurar CORS para frontend acessar a API
origins = [
    "http://localhost",
    "http://localhost:8501",  # padrão Streamlit local
    # adicionar domínios permitidos aqui (ex: frontend deploy)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(cliente_routes.router, prefix="/clientes", tags=["Clientes"])
app.include_router(produto_routes.router, prefix="/produtos", tags=["Produtos"])
app.include_router(servico_routes.router, prefix="/servicos", tags=["Serviços"])
app.include_router(venda_routes.router, prefix="/vendas", tags=["Vendas"])
app.include_router(despesa_routes.router, prefix="/despesas", tags=["Despesas"])
app.include_router(agendamento_routes.router, prefix="/agendamentos", tags=["Agendamentos"])
app.include_router(usuario_routes.router, prefix="/usuarios", tags=["Usuários"])
app.include_router(backup.router, prefix="/backup", tags=["Backup"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(relatorio.router, prefix="/relatorios", tags=["Relatórios"])

@app.get("/")
async def root():
    return {"message": "API Studio Depilação - Online"}


