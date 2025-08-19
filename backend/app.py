 from fastapi import FastAPI
 from fastapi.middleware.cors import CORSMiddleware
 from backend.config.database import engine, Base
 from dotenv import load_dotenv
 import os
 
 load_dotenv()
 
 # IMPORTANTE: importar models para registrar no metadata
-from backend.models import (
+from .models import (
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
