# Usar imagem base oficial do Python
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar requirements primeiro (para otimizar cache)
COPY backend/requirements.txt .

# Atualizar pip e instalar dependências
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o backend para o container
COPY backend/ .

# Expõe a porta do FastAPI
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
