
import streamlit as st
import requests
from datetime import date

API_URL = "http://localhost:8000"  # ajuste conforme seu backend

def despesas():
    st.subheader("📉 Registro de Despesas")

    with st.form("form_despesa", clear_on_submit=True):
        data_desp = st.date_input("Data da Despesa", date.today(), format="DD/MM/YYYY")
        descricao = st.text_input("Descrição")
        valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f")
        if st.form_submit_button("Salvar Despesa"):
            payload = {
                "data": data_desp.strftime("%Y-%m-%d"),
                "descricao": descricao,
                "valor": valor
            }
            try:
                res = requests.post(f"{API_URL}/despesas/", json=payload)
                res.raise_for_status()
                st.success("Despesa registrada!")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Erro ao salvar despesa: {e}")

    # Listar despesas
    try:
        res = requests.get(f"{API_URL}/despesas/")
        res.raise_for_status()
        despesas = res.json()
    except Exception as e:
        st.error(f"Erro ao carregar despesas: {e}")
        return

    if despesas:
        st.write("### Despesas Registradas")
        for despesa in despesas:
            col1, col2, col3, col4 = st.columns([1, 3, 2, 1])
            col1.write(despesa["id"])
            col2.write(despesa["descricao"])
            col3.write(f"R$ {despesa['valor']:.2f}")
            if col4.button("❌", key=f"del_{despesa['id']}"):
                try:
                    res = requests.delete(f"{API_URL}/despesas/{despesa['id']}")
                    res.raise_for_status()
                    st.success(f"Despesa ID {despesa['id']} excluída!")
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Erro ao excluir despesa: {e}")
    else:
        st.info("Nenhuma despesa registrada.")
