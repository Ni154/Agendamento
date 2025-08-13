# Imagem base oficial do Python
FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Instala pacotes de sistema necessários para o psycopg2 e outros
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia apenas o requirements.txt primeiro para aproveitar cache no rebuild
COPY backend/requirements.txt /app/requirements.txt

# Instala dependências do Python
RUN python -m ensurepip --upgrade && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copia todo o código do backend
COPY backend/ /app/

# Expõe a porta que o Uvicorn vai usar
EXPOSE 8000

# Comando para rodar o backend FastAPI no Railway
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
