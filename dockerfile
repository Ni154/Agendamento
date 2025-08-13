# Usar Python 3.11 como base
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Evitar prompts de interação
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copiar arquivos de dependências primeiro
COPY requirements.txt .

# Atualizar pip e instalar dependências
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copiar todo o código do backend
COPY . .

# Expor a porta usada pelo FastAPI
EXPOSE 8000

# Comando para rodar o backend
CMD ["uvicorn", "main:app", "--host",]()
