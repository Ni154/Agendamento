import streamlit as st
import requests

API_URL = "http://localhost:8000"  # ajuste conforme seu backend

def vendas():
    st.subheader("💰 Gestão de Vendas")

    # Buscar agendamentos para pré-venda
    agendamentos = []
    try:
        res = requests.get(f"{API_URL}/agendamentos/")
        res.raise_for_status()
        agendamentos = res.json()
    except Exception as e:
        st.error(f"Erro ao buscar agendamentos: {e}")

    opcoes_agendamento = ["Nova Venda"] + [f"{a['id']} - {a['cliente_nome']} - {a['data']} {a['hora']}" for a in agendamentos]
    selecao = st.selectbox("Selecionar agendamento para pré-venda ou iniciar nova venda", opcoes_agendamento)

    venda_id = None
    itens_venda = []
    total_venda = 0.0
    cliente_id = None

    if selecao != "Nova Venda":
        agendamento_id = int(selecao.split(" - ")[0])
        # Buscar dados do agendamento para iniciar venda
        try:
            res = requests.get(f"{API_URL}/agendamentos/{agendamento_id}")
            res.raise_for_status()
            agendamento = res.json()
            cliente_id = agendamento["cliente_id"]
            # Monta os itens iniciais só com serviços do agendamento
            servicos = agendamento.get("servicos", [])
            itens_venda = []
            for s in servicos:
                itens_venda.append({
                    "tipo": "servico",
                    "item_id": s["id"],
                    "nome": s["nome"],
                    "quantidade": 1,
                    "preco": s["valor"]
                })
        except Exception as e:
            st.error(f"Erro ao carregar agendamento: {e}")

    # Seleção de cliente (se nova venda)
    if cliente_id is None:
        try:
            res = requests.get(f"{API_URL}/clientes/")
            res.raise_for_status()
            clientes = res.json()
            clientes_dict = {f'{c["id"]} - {c["nome"]}': c["id"] for c in clientes}
            selecionado = st.selectbox("Selecionar Cliente", [""] + list(clientes_dict.keys()))
            if selecionado != "":
                cliente_id = clientes_dict[selecionado]
        except Exception as e:
            st.error(f"Erro ao carregar clientes: {e}")

    # Seleção e adição de itens
    st.markdown("---")
    st.write("### Itens da Venda")

    # Carregar produtos e serviços para seleção
    produtos = []
    servicos = []
    try:
        res_p = requests.get(f"{API_URL}/produtos/")
        res_p.raise_for_status()
        produtos = res_p.json()
        res_s = requests.get(f"{API_URL}/servicos/")
        res_s.raise_for_status()
        servicos = res_s.json()
    except Exception as e:
        st.error(f"Erro ao carregar produtos ou serviços: {e}")

    tipo_item = st.selectbox("Tipo de item para adicionar", ["produto", "servico"])
    if tipo_item == "produto":
        itens_disponiveis = {p["nome"]: p for p in produtos}
    else:
        itens_disponiveis = {s["nome"]: s for s in servicos}

    item_nome = st.selectbox("Selecionar item", [""] + list(itens_disponiveis.keys()))
    quantidade = st.number_input("Quantidade", min_value=1, step=1, value=1)

    if st.button("Adicionar item"):
        if item_nome and cliente_id:
            item = itens_disponiveis[item_nome]
            # Verifica se item já está na venda para somar quantidade
            achou = False
            for iv in itens_venda:
                if iv["tipo"] == tipo_item and iv["item_id"] == item["id"]:
                    iv["quantidade"] += quantidade
                    achou = True
                    break
            if not achou:
                itens_venda.append({
                    "tipo": tipo_item,
                    "item_id": item["id"],
                    "nome": item_nome,
                    "quantidade": quantidade,
                    "preco": item["preco_venda"] if tipo_item == "produto" else item["valor"]
                })
            st.experimental_rerun()
        else:
            st.error("Selecione um cliente e um item para adicionar.")

    # Mostrar tabela dos itens da venda
    if itens_venda:
        total_venda = sum(i["quantidade"] * i["preco"] for i in itens_venda)
        for idx, iv in enumerate(itens_venda):
            col1, col2, col3, col4, col5 = st.columns([4, 2, 2, 2, 1])
            col1.write(iv["nome"])
            col2.write(iv["quantidade"])
            col3.write(f"R$ {iv['preco']:.2f}")
            col4.write(f"R$ {iv['quantidade'] * iv['preco']:.2f}")
            if col5.button("❌", key=f"del_{idx}"):
                itens_venda.pop(idx)
                st.experimental_rerun()

        st.markdown(f"**Total da Venda: R$ {total_venda:.2f}**")

        forma_pagamento = st.selectbox("Forma de pagamento", ["Dinheiro", "Cartão", "Pix", "Outro"])
        if st.button("Finalizar Venda"):
            if cliente_id is None:
                st.error("Selecione um cliente antes de finalizar.")
            else:
                # Monta payload para salvar venda
                venda_payload = {
                    "cliente_id": cliente_id,
                    "total": total_venda,
                    "forma_pagamento": forma_pagamento,
                    "itens": [{"tipo": i["tipo"], "item_id": i["item_id"], "quantidade": i["quantidade"], "preco": i["preco"]} for i in itens_venda]
                }
                try:
                    res = requests.post(f"{API_URL}/vendas/", json=venda_payload)
                    res.raise_for_status()
                    st.success("Venda finalizada com sucesso!")
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Erro ao finalizar venda: {e}")
    else:
        st.info("Nenhum item adicionado à venda.")

