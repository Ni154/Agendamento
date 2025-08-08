import streamlit as st
import requests
from datetime import datetime, date

API_URL = "http://localhost:8000"  # Ajuste conforme seu backend

def formatar_data_br(data_iso):
    try:
        return datetime.strptime(data_iso, "%Y-%m-%d").strftime("%d/%m/%Y")
    except:
        return data_iso

def agendamento():
    st.subheader("📅 Agendamentos")

    # Formulário para criar novo agendamento
    with st.form("form_agendamento", clear_on_submit=True):
        # Buscar clientes para seleção
        try:
            res = requests.get(f"{API_URL}/clientes/")
            res.raise_for_status()
            clientes = res.json()
        except Exception as e:
            st.error(f"Erro ao carregar clientes: {e}")
            clientes = []

        cliente_dict = {c["nome"]: c["id"] for c in clientes}
        cliente_nome = st.selectbox("Cliente", [""] + list(cliente_dict.keys()))

        data_agendamento = st.date_input("Data do Agendamento", min_value=date.today())
        hora_agendamento = st.time_input("Hora do Agendamento")

        servicos = st.text_area("Serviços (separe por vírgula)")

        if st.form_submit_button("Agendar"):
            if not cliente_nome:
                st.error("Selecione um cliente.")
            elif not servicos.strip():
                st.error("Informe ao menos um serviço.")
            else:
                try:
                    cliente_id = cliente_dict[cliente_nome]
                    payload = {
                        "cliente_id": cliente_id,
                        "data": data_agendamento.strftime("%Y-%m-%d"),
                        "hora": hora_agendamento.strftime("%H:%M"),
                        "servicos": servicos,
                        "status": "Agendado"
                    }
                    res_post = requests.post(f"{API_URL}/agendamentos/", json=payload)
                    res_post.raise_for_status()
                    st.success("Agendamento criado com sucesso!")
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Erro ao criar agendamento: {e}")

    # Mostrar lista de agendamentos futuros
    st.markdown("---")
    st.write("### Agendamentos futuros")

    try:
        res_ag = requests.get(f"{API_URL}/agendamentos/")
        res_ag.raise_for_status()
        agendamentos = res_ag.json()
    except Exception as e:
        st.error(f"Erro ao carregar agendamentos: {e}")
        agendamentos = []

    if agendamentos:
        for ag in agendamentos:
            st.info(
                f"📅 {formatar_data_br(ag['data'])} 🕒 {ag['hora']} | 👤 Cliente ID: {ag['cliente_id']} | Serviços: {ag['servicos']} | Status: {ag['status']}"
            )
    else:
        st.info("Nenhum agendamento cadastrado.")

