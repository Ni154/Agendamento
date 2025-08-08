import streamlit as st
import requests

API_URL = "http://localhost:8000"  # Ajuste conforme seu backend

def cadastro_servicos():
    st.subheader("💆 Cadastro e Gerenciamento de Serviços")

    # Formulário para cadastrar novo serviço
    with st.form("form_servico", clear_on_submit=True):
        nome = st.text_input("Nome do serviço")
        unidade = st.text_input("Unidade (ex: sessão, hora)")
        quantidade = st.number_input("Quantidade disponível", min_value=0, step=1)
        valor = st.number_input("Valor do serviço (R$)", min_value=0.0, format="%.2f")

        if st.form_submit_button("Salvar Serviço"):
            if not nome or not unidade:
                st.error("Preencha o nome e a unidade do serviço.")
            else:
                payload = {
                    "nome": nome,
                    "unidade": unidade,
                    "quantidade": quantidade,
                    "valor": valor
                }
                try:
                    res = requests.post(f"{API_URL}/servicos/", json=payload)
                    res.raise_for_status()
                    st.success("Serviço cadastrado com sucesso!")
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Erro ao cadastrar serviço: {e}")

    # Listagem dos serviços cadastrados
    st.markdown("---")
    st.write("### Serviços cadastrados")

    try:
        res = requests.get(f"{API_URL}/servicos/")
        res.raise_for_status()
        servicos = res.json()
    except Exception as e:
        st.error(f"Erro ao carregar serviços: {e}")
        servicos = []

    if servicos:
        for s in servicos:
            col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
            col1.write(s["nome"])
            col2.write(s["unidade"])
            col3.write(s["quantidade"])
            col4.write(f"R$ {s['valor']:.2f}")
    else:
        st.info("Nenhum serviço cadastrado.")

