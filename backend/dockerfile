# Imagem base Python oficial
FROM python:3.10-slim

# Evitar prompts durante instalação
ENV DEBIAN_FRONTEND=noninteractive

# Atualiza pacotes e instala dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libopenjp2-7-dev \
    libtiff5-dev \
    tk-dev \
    tcl-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Criar diretório de trabalho
WORKDIR /app

# Copiar requirements primeiro (para otimizar cache)
COPY requirements.txt .

# Instalar pacotes Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar o código do projeto
COPY . .

# Definir PYTHONPATH para que o backend seja encontrado
ENV PYTHONPATH=/app

# Expõe a porta que o Uvicorn vai usar
EXPOSE 8000

# Comando de inicialização
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
