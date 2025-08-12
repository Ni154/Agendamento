import streamlit as st
import requests

API_URL = "https://seu-backend.onrender.com"  # URL do backend

def vendas_page():
    st.title("💰 Módulo de Vendas")

    st.subheader("📋 Agendamentos disponíveis para venda")
    agendamentos = requests.get(f"{API_URL}/agendamentos/pendentes").json()

    if not agendamentos:
        st.info("Nenhum agendamento disponível para conversão em venda.")
        return

    opcoes = {f"{a['id']} - {a['cliente_nome']} ({a['data']})": a for a in agendamentos}
    selecao = st.selectbox("Selecione um agendamento", list(opcoes.keys()))

    agendamento_selecionado = opcoes[selecao]

    st.write(f"**Cliente:** {agendamento_selecionado['cliente_nome']}")
    st.write(f"**Serviço:** {agendamento_selecionado['servico_nome']}")
    st.write(f"**Data:** {agendamento_selecionado['data']}")

    produtos = requests.get(f"{API_URL}/produtos").json()
    produtos_selecionados = st.multiselect(
        "Adicione produtos à venda",
        options=[p["nome"] for p in produtos]
    )

    valor_total = agendamento_selecionado["valor"]
    for prod in produtos:
        if prod["nome"] in produtos_selecionados:
            valor_total += prod["preco"]

    st.write(f"💵 Valor total: R$ {valor_total:.2f}")

    if st.button("Finalizar Venda"):
        payload = {
            "agendamento_id": agendamento_selecionado["id"],
            "produtos": produtos_selecionados,
            "valor_total": valor_total
        }
        response = requests.post(f"{API_URL}/vendas", json=payload)
        if response.status_code == 201:
            st.success("Venda finalizada com sucesso!")
        else:
            st.error("Erro ao finalizar venda.")
