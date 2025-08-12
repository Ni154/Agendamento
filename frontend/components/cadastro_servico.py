import streamlit as st
from frontend.utils import api_get, api_post, api_put, api_delete, token_header

API_PREFIX = "/servicos"

def listar_servicos():
    return api_get(API_PREFIX)

def cadastrar_servico_form():
    st.subheader("Novo Serviço")
    nome = st.text_input("Nome do serviço")
    unidade = st.text_input("Unidade (ex: sessão)")
    quantidade = st.number_input("Quantidade disponível", min_value=0, value=1)
    valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f")
    if st.button("Salvar Serviço"):
        payload = {"nome": nome, "unidade": unidade, "quantidade": quantidade, "valor": valor}
        res = api_post(API_PREFIX + "/", payload, token_header().get("Authorization"))
        if res:
            st.success("Serviço cadastrado")
            st.experimental_rerun()
        else:
            st.error("Erro ao cadastrar serviço.")

def servicos_page():
    st.title("💆 Serviços")

    st.subheader("Serviços cadastrados")
    servicos = listar_servicos()
    if servicos:
        for s in servicos:
            cols = st.columns([3,1,1,1])
            cols[0].write(s.get("nome"))
            cols[1].write(s.get("unidade") or "-")
            cols[2].write(int(s.get("quantidade", 0)))
            cols[3].write(f"R$ {float(s.get('valor', 0)):.2f}")
            if cols[3].button("Editar", key=f"edit_s_{s['id']}"):
                st.session_state["servico_edit_id"] = s["id"]
                st.experimental_rerun()
        servico_edit_id = st.session_state.get("servico_edit_id")
        if servico_edit_id:
            st.markdown("---")
            st.subheader("Editar serviço")
            serv = next((x for x in servicos if x["id"] == servico_edit_id), None)
            if serv:
                novo_nome = st.text_input("Nome", value=serv["nome"])
                nova_unidade = st.text_input("Unidade", value=serv.get("unidade") or "")
                nova_qtd = st.number_input("Quantidade", min_value=0, value=int(serv.get("quantidade", 0)))
                novo_valor = st.number_input("Valor (R$)", min_value=0.0, value=float(serv.get("valor", 0)), format="%.2f")
                if st.button("Atualizar"):
                    payload = {"nome": novo_nome, "unidade": nova_unidade, "quantidade": nova_qtd, "valor": novo_valor}
                    res = api_put(f"{API_PREFIX}/{servico_edit_id}", payload, token_header().get("Authorization"))
                    if res:
                        st.success("Serviço atualizado")
                        st.session_state.pop("servico_edit_id", None)
                        st.experimental_rerun()
                    else:
                        st.error("Erro ao atualizar.")
                if st.button("Excluir Serviço"):
                    ok = api_delete(f"{API_PREFIX}/{servico_edit_id}", token_header().get("Authorization"))
                    if ok:
                        st.success("Serviço excluído")
                        st.session_state.pop("servico_edit_id", None)
                        st.experimental_rerun()
                    else:
                        st.error("Erro ao excluir.")
    else:
        st.info("Nenhum serviço cadastrado.")

    with st.expander("Cadastrar novo serviço"):
        cadastrar_servico_form()

if __name__ == "__main__":
    servicos_page()
