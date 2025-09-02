# base
FROM python:3.12-slim

# diretório de trabalho
WORKDIR /app

# dependências
COPY pyproject.toml poetry.lock* requirements.txt* /app/
# (instale com poetry ou pip, conforme usa)
# Exemplo pip:
RUN pip install --no-cache-dir -r requirements.txt

# copie o código
COPY backend/ /app/backend/

# (se você ainda tiver um app.py na raiz E quiser mantê-lo por qualquer motivo)
# COPY app.py /app/app.py

# melhore resolução de imports
ENV PYTHONPATH=/app

# start
CMD ["uvicorn","backend.app:app","--host","0.0.0.0","--port","8000"]
