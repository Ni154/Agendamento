import streamlit as st
import requests

API_URL = "http://localhost:8000"  # Ajuste conforme seu backend

def cadastro_produtos():
    st.subheader("📦 Cadastro e Gerenciamento de Produtos")

    # Formulário para cadastrar novo produto
    with st.form("form_produto", clear_on_submit=True):
        nome = st.text_input("Nome do produto")
        quantidade = st.number_input("Quantidade em estoque", min_value=0, step=1)
        preco_venda = st.number_input("Preço de venda (R$)", min_value=0.0, format="%.2f")

        if st.form_submit_button("Salvar Produto"):
            if not nome:
                st.error("Informe o nome do produto.")
            else:
                payload = {
                    "nome": nome,
                    "quantidade": quantidade,
                    "preco_venda": preco_venda
                }
                try:
                    res = requests.post(f"{API_URL}/produtos/", json=payload)
                    res.raise_for_status()
                    st.success("Produto cadastrado com sucesso!")
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Erro ao cadastrar produto: {e}")

    # Listar produtos cadastrados
    st.markdown("---")
    st.write("### Produtos cadastrados")

    try:
        res = requests.get(f"{API_URL}/produtos/")
        res.raise_for_status()
        produtos = res.json()
    except Exception as e:
        st.error(f"Erro ao carregar produtos: {e}")
        produtos = []

    if produtos:
        for p in produtos:
            col1, col2, col3 = st.columns([3, 1, 2])
            col1.write(p["nome"])
            col2.write(f"{p['quantidade']}")
            col3.write(f"R$ {p['preco_venda']:.2f}")
    else:
        st.info("Nenhum produto cadastrado.")

