FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia apenas requirements primeiro (cache build)
COPY backend/requirements.txt /app/requirements.txt

# Instala pip e dependências Python
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copia código do backend
COPY backend/ /app/

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
