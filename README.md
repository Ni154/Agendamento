# Studio App — Backend (Flask)

## Rodando local

```bash
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt

# crie um .env na raiz (ou configure no PyCharm):
# DATABASE_URL=postgresql://user:pass@host:port/db?sslmode=require

python backend/app.py
# Abra: http://127.0.0.1:5000/api/health
# Debug DB: http://127.0.0.1:5000/api/debug/db
```

## Deploy no Railway

- Crie serviço "PostgreSQL" e copie a **Public Connection URL** para a variável `DATABASE_URL` do serviço do backend.
- Adicione `SECRET_KEY` em Variables.
- Start command: `gunicorn "backend.app:app" --workers=2 --threads=4 --timeout=120`
- `requirements.txt` e `Procfile` estão em `backend/`.

## Endpoints

- `GET /api/health`
- `GET /api/debug/db`
- `GET /api/agendamentos/`
- `POST /api/agendamentos/`
- `PUT /api/agendamentos/<id>/status`
