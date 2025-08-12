import streamlit as st
import requests

API_URL = "https://seu-backend.onrender.com"

def produtos_page():
    st.title("📦 Gerenciamento de Produtos")

    with st.form("form_produto"):
        nome = st.text_input("Nome do Produto")
        preco = st.number_input("Preço", min_value=0.0, step=0.01)
        estoque = st.number_input("Quantidade em Estoque", min_value=0)
        categoria = st.selectbox("Categoria", ["Cosmético", "Equipamento", "Outros"])

        if st.form_submit_button("Salvar"):
            payload = {
                "nome": nome,
                "preco": preco,
                "estoque": estoque,
                "categoria": categoria
            }
            response = requests.post(f"{API_URL}/produtos", json=payload)
            if response.status_code == 201:
                st.success("Produto cadastrado com sucesso!")
            else:
                st.error("Erro ao cadastrar produto.")

    st.subheader("📜 Lista de Produtos")
    produtos = requests.get(f"{API_URL}/produtos").json()

    if produtos:
        st.table(produtos)
    else:
        st.info("Nenhum produto cadastrado.")
