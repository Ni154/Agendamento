import requests
import streamlit as st
from datetime import datetime

API_URL = st.secrets.get("API_URL") or "http://localhost:8000"  # Ajuste para seu backend

def api_get(endpoint, token=None):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        resp = requests.get(f"{API_URL}{endpoint}", headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        st.error(f"Erro na requisição GET: {e}")
        return None

def api_post(endpoint, data, token=None):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        resp = requests.post(f"{API_URL}{endpoint}", json=data, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        st.error(f"Erro na requisição POST: {e}")
        return None

def formatar_data_br(data_iso):
    try:
        return datetime.strptime(data_iso, "%Y-%m-%d").strftime("%d/%m/%Y")
    except Exception:
        return data_iso

def limpa_campo(texto):
    return texto.strip() if texto else texto

def verifica_login():
    if not st.session_state.get("login", False):
        st.warning("Você precisa estar logado para acessar esta funcionalidade.")
        st.stop()

def token_header():
    token = st.session_state.get("token")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

