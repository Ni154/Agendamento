# Escolhe uma imagem oficial do Python
FROM python:3.11-slim

# Define diretório de trabalho dentro do container
WORKDIR /app

# Instala dependências de sistema necessárias para o psycopg2 e outros pacotes
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia arquivos de dependências primeiro (para aproveitar cache no rebuild)
COPY backend/requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia o código do backend
COPY backend/ .

# Expõe a porta que o Uvicorn vai usar
EXPOSE 8000

# Comando para rodar a aplicação no Railway
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
