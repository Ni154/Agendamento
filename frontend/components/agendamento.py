import streamlit as st
from datetime import datetime, date
from frontend.utils import api_get, api_post, api_delete, token_header, formatar_data_br

API_PREFIX = "/agendamentos"
CLIENTES_PREFIX = "/clientes"
SERVICOS_PREFIX = "/servicos"

def listar_agendamentos():
    return api_get(API_PREFIX)

def criar_agendamento(payload):
    return api_post(API_PREFIX + "/", payload, token_header().get("Authorization"))

def deletar_agendamento(agendamento_id):
    return api_delete(f"{API_PREFIX}/{agendamento_id}", token_header().get("Authorization"))

def agendamento_page():
    st.title("📅 Agendamentos")

    tab = st.tabs(["Listar Agendamentos", "Novo Agendamento"])[0]
    with tab:
        st.subheader("Agendamentos futuros")
        ags = listar_agendamentos() or []
        if ags:
            for ag in ags:
                col1, col2, col3, col4 = st.columns([2,3,2,2])
                col1.write(formatar_data_br(ag.get("data")))
                col2.write(ag.get("cliente_nome") or f"ID {ag.get('cliente_id')}")
                col3.write(ag.get("hora"))
                col4.write(ag.get("status"))
                if col4.button(f"Reagendar {ag['id']}", key=f"reag_{ag['id']}"):
                    st.session_state["reagendar_id"] = ag["id"]
                    st.experimental_rerun()
                if col4.button(f"Cancelar {ag['id']}", key=f"cancel_{ag['id']}"):
                    st.session_state["cancelar_id"] = ag["id"]
                    st.experimental_rerun()
                if col4.button(f"🗑 Deletar {ag['id']}", key=f"del_{ag['id']}"):
                    ok = deletar_agendamento(ag["id"])
                    if ok:
                        st.success("Agendamento deletado")
                        st.experimental_rerun()
                    else:
                        st.error("Erro ao deletar")
                st.markdown("---")
        else:
            st.info("Nenhum agendamento encontrado.")

        # Reagendar / cancelar flow
        if st.session_state.get("reagendar_id"):
            ag_id = st.session_state["reagendar_id"]
            st.subheader("🔄 Reagendar")
            st.write(f"Agendamento ID: {ag_id}")
            nova_data = st.date_input("Nova data", value=date.today())
            nova_hora = st.text_input("Nova hora (ex: 14:30)")
            if st.button("Confirmar Reagendamento"):
                payload = {"data": nova_data.strftime("%Y-%m-%d"), "hora": nova_hora}
                res = api_post(f"{API_PREFIX}/{ag_id}/reagendar", payload, token_header().get("Authorization"))
                if res:
                    st.success("Reagendamento confirmado")
                else:
                    st.error("Erro no reagendamento")
                st.session_state.pop("reagendar_id", None)
                st.experimental_rerun()
            if st.button("Cancelar"):
                st.session_state.pop("reagendar_id", None)
                st.experimental_rerun()

        if st.session_state.get("cancelar_id"):
            ag_id = st.session_state["cancelar_id"]
            st.subheader("❌ Cancelar Agendamento")
            if st.button("Confirmar Cancelamento"):
                res = api_post(f"{API_PREFIX}/{ag_id}/cancelar", {}, token_header().get("Authorization"))
                if res:
                    st.success("Agendamento cancelado")
                else:
                    st.error("Erro ao cancelar")
                st.session_state.pop("cancelar_id", None)
                st.experimental_rerun()
            if st.button("Voltar"):
                st.session_state.pop("cancelar_id", None)
                st.experimental_rerun()

    with st.tab("Novo Agendamento"):
        st.subheader("Criar novo agendamento")

        # Load clientes e serviços para selects
        clientes = api_get(CLIENTES_PREFIX) or []
        servicos = api_get(SERVICOS_PREFIX) or []

        clientes_dict = {f"{c['id']} - {c['nome']}": c['id'] for c in clientes}
        servicos_dict = {f"{s['id']} - {s['nome']}": s['id'] for s in servicos}

        cliente_sel = st.selectbox("Selecione o Cliente", [""] + list(clientes_dict.keys()))
        data_ag = st.date_input("Data do Agendamento", value=date.today())
        hora_ag = st.time_input("Hora do Agendamento")
        serv_selecionados = st.multiselect("Serviços", [""] + list(servicos_dict.keys()))
        status = st.selectbox("Status", ["Agendado", "Confirmado", "Concluído", "Cancelado"])

        if st.button("Salvar Agendamento"):
            if cliente_sel == "" or not serv_selecionados:
                st.error("Selecione cliente e ao menos um serviço")
            else:
                cliente_id = clientes_dict[cliente_sel]
                serv_ids = [servicos_dict[s] for s in serv_selecionados if s]
                servicos_str = ", ".join([s.split(" - ",1)[1] for s in serv_selecionados if s])
                payload = {
                    "cliente_id": cliente_id,
                    "data": data_ag.strftime("%Y-%m-%d"),
                    "hora": hora_ag.strftime("%H:%M"),
                    "servicos": servicos_str,
                    "status": status
                }
                res = criar_agendamento(payload)
                if res:
                    st.success("Agendamento criado")
                    st.experimental_rerun()
                else:
                    st.error("Erro ao criar agendamento")

if __name__ == "__main__":
    agendamento_page()
