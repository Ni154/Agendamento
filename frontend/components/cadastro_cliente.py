import streamlit as st
from frontend.utils import api_get, api_post, api_delete, token_header
from datetime import datetime

API_PREFIX = "/clientes"

def listar_clientes():
    return api_get(API_PREFIX)

def criar_cliente_payload_from_form():
    nome = st.text_input("Nome completo")
    telefone = st.text_input("Telefone")
    nascimento = st.text_input("Data de nascimento (YYYY-MM-DD)", placeholder="1980-12-31")
    hora_agendada = st.text_input("Hora agendada (ex: 14:30)")
    instagram = st.text_input("Instagram")
    # Campos extras (simplificados)
    if st.button("Salvar Cliente"):
        payload = {
            "nome": nome,
            "telefone": telefone,
            "nascimento": nascimento,
            "hora_agendada": hora_agendada,
            "instagram": instagram
        }
        res = api_post(API_PREFIX + "/", payload, token_header().get("Authorization"))
        if res:
            st.success("Cliente cadastrado com sucesso!")
            st.experimental_rerun()
        else:
            st.error("Erro ao cadastrar cliente.")

def clientes_page():
    st.title("🧍 Clientes")

    tab = st.tabs(["Listar / Buscar", "Novo Cliente"])[0]  # use first tab area
    with tab:
        st.subheader("Lista de clientes")
        clientes = listar_clientes()
        if clientes:
            for c in clientes:
                cols = st.columns([4,2,2])
                cols[0].write(f"**{c.get('nome')}**")
                cols[1].write(c.get('telefone') or "-")
                cols[2].write(c.get('nascimento') and datetime.strptime(c.get('nascimento'), "%Y-%m-%d").strftime("%d/%m/%Y") or "-")
                if cols[2].button("Ver / Excluir", key=f"ver_{c['id']}"):
                    st.session_state["cliente_ver_id"] = c["id"]
                    st.experimental_rerun()
            # Ver cliente selecionado
            cliente_ver_id = st.session_state.get("cliente_ver_id")
            if cliente_ver_id:
                st.markdown("---")
                st.subheader("Detalhes do cliente")
                cliente = next((x for x in clientes if x["id"] == cliente_ver_id), None)
                if cliente:
                    st.write(f"Nome: {cliente.get('nome')}")
                    st.write(f"Telefone: {cliente.get('telefone')}")
                    st.write(f"Nascimento: {cliente.get('nascimento')}")
                    if st.button("Excluir Cliente"):
                        ok = api_delete(f"{API_PREFIX}/{cliente_ver_id}", token_header().get("Authorization"))
                        if ok:
                            st.success("Cliente excluído")
                            st.session_state.pop("cliente_ver_id", None)
                            st.experimental_rerun()
                        else:
                            st.error("Erro ao excluir.")
        else:
            st.info("Nenhum cliente cadastrado.")

    with st.expander("Cadastrar novo cliente"):
        criar_cliente_payload_from_form()

if __name__ == "__main__":
    clientes_page()
