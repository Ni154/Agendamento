import streamlit as st
import requests
from datetime import date

API_URL = "https://seu-backend.onrender.com"

def despesas_page():
    st.title("📉 Controle de Despesas")

    with st.form("form_despesa"):
        descricao = st.text_input("Descrição da Despesa")
        valor = st.number_input("Valor", min_value=0.0, step=0.01)
        data = st.date_input("Data", value=date.today())
        categoria = st.selectbox("Categoria", ["Aluguel", "Água", "Luz", "Internet", "Produtos", "Outros"])

        if st.form_submit_button("Salvar"):
            payload = {
                "descricao": descricao,
                "valor": valor,
                "data": str(data),
                "categoria": categoria
            }
            response = requests.post(f"{API_URL}/despesas", json=payload)
            if response.status_code == 201:
                st.success("Despesa registrada com sucesso!")
            else:
                st.error("Erro ao registrar despesa.")

    st.subheader("📜 Histórico de Despesas")
    despesas = requests.get(f"{API_URL}/despesas").json()

    if despesas:
        st.table(despesas)
    else:
        st.info("Nenhuma despesa cadastrada.")
