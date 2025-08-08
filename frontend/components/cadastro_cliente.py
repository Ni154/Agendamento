import streamlit as st
import requests
from datetime import datetime
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io
import base64

API_URL = "http://localhost:8000"  # Ajuste a URL da API conforme seu ambiente

def formatar_data_br(data_iso):
    try:
        return datetime.strptime(data_iso, "%Y-%m-%d").strftime("%d/%m/%Y")
    except:
        return data_iso

def cadastro_cliente():
    st.subheader("🧍 Cadastro e Gerenciamento de Clientes")

    # Buscar clientes do backend
    try:
        res = requests.get(f"{API_URL}/clientes/")
        res.raise_for_status()
        clientes = res.json()
    except Exception as e:
        st.error(f"Erro ao buscar clientes: {e}")
        clientes = []

    clientes_dict = {c["nome"]: c["id"] for c in clientes}

    col1, col2 = st.columns([2, 3])

    with col1:
        with st.form("form_cliente", clear_on_submit=True):
            nome = st.text_input("Nome completo")
            telefone = st.text_input("Telefone")
            nascimento_str = st.text_input("Data de nascimento (DD/MM/AAAA)", placeholder="31/12/1980")
            hora_agendada = st.text_input("Hora agendada (ex: 14:30)")
            instagram = st.text_input("Instagram")
            cantor = st.text_input("Cantor favorito")
            bebida = st.text_input("Bebida favorita")
            epilacao = st.radio("Já fez epilação na cera?", ["SIM", "NÃO"])
            alergia = st.radio("Possui alergia?", ["SIM", "NÃO"])
            qual_alergia = st.text_input("Qual alergia?") if alergia == "SIM" else ""
            problemas_pele = st.radio("Problemas de pele?", ["SIM", "NÃO"])
            tratamento = st.radio("Tratamento dermatológico?", ["SIM", "NÃO"])
            tipo_pele = st.radio("Tipo de pele", ["SECA", "OLEOSA", "NORMAL"])
            hidrata = st.radio("Hidrata a pele?", ["SIM", "NÃO"])
            gravida = st.radio("Está grávida?", ["SIM", "NÃO"])
            medicamento = st.radio("Uso de medicamentos?", ["SIM", "NÃO"])
            qual_medicamento = st.text_input("Qual medicamento?") if medicamento == "SIM" else ""
            uso = st.radio("DIU ou marca-passo?", ["DIU", "Marca-passo", "Nenhum"])
            diabete = st.radio("Diabetes?", ["SIM", "NÃO"])
            pelos_encravados = st.radio("Pelos encravados?", ["SIM", "NÃO"])
            cirurgia = st.radio("Cirurgia recente?", ["SIM", "NÃO"])
            foliculite = st.radio("Foliculite?", ["SIM", "NÃO"])
            qual_foliculite = st.text_input("Qual foliculite?") if foliculite == "SIM" else ""
            problema_extra = st.radio("Outro problema?", ["SIM", "NÃO"])
            qual_problema = st.text_input("Qual problema?") if problema_extra == "SIM" else ""
            autorizacao_imagem = st.radio("Autoriza uso de imagem?", ["SIM", "NÃO"])

            st.write("Assinatura Digital")
            assinatura_canvas = st_canvas(
                fill_color="rgba(0,0,0,0)",
                stroke_width=2,
                stroke_color="#000",
                background_color="#eee",
                height=150,
                width=400,
                drawing_mode="freedraw"
            )

            if st.form_submit_button("Salvar Cliente"):
                try:
                    nascimento = datetime.strptime(nascimento_str, "%d/%m/%Y").date()
                except Exception:
                    st.error("Data de nascimento inválida. Use o formato DD/MM/AAAA.")
                    st.stop()

                assinatura = None
                if assinatura_canvas.image_data is not None:
                    img = Image.fromarray(assinatura_canvas.image_data.astype('uint8'), 'RGBA')
                    buffer = io.BytesIO()
                    img.save(buffer, format="PNG")
                    assinatura = base64.b64encode(buffer.getvalue()).decode("utf-8")

                cliente_data = {
                    "nome": nome,
                    "telefone": telefone,
                    "nascimento": nascimento.strftime("%Y-%m-%d"),
                    "hora_agendada": hora_agendada,
                    "instagram": instagram,
                    "cantor": cantor,
                    "bebida": bebida,
                    "epilacao": epilacao,
                    "alergia": alergia,
                    "qual_alergia": qual_alergia,
                    "problemas_pele": problemas_pele,
                    "tratamento": tratamento,
                    "tipo_pele": tipo_pele,
                    "hidrata": hidrata,
                    "gravida": gravida,
                    "medicamento": medicamento,
                    "qual_medicamento": qual_medicamento,
                    "uso": uso,
                    "diabete": diabete,
                    "pelos_encravados": pelos_encravados,
                    "cirurgia": cirurgia,
                    "foliculite": foliculite,
                    "qual_foliculite": qual_foliculite,
                    "problema_extra": problema_extra,
                    "qual_problema": qual_problema,
                    "autorizacao_imagem": autorizacao_imagem,
                    "assinatura": assinatura
                }

                try:
                    res_post = requests.post(f"{API_URL}/clientes/", json=cliente_data)
                    res_post.raise_for_status()
                    st.success("Cliente cadastrado com sucesso!")
                    st.experimental_rerun()
                except Exception as e:
                    st.error(f"Erro ao salvar cliente: {e}")

    with col2:
        st.write("### Clientes Cadastrados")
        nomes = list(clientes_dict.keys())
        cliente_selecionado = st.selectbox("Selecionar cliente para visualizar ou excluir", [""] + nomes)

        if cliente_selecionado:
            cliente_id = clientes_dict[cliente_selecionado]
            try:
                res_det = requests.get(f"{API_URL}/clientes/{cliente_id}")
                res_det.raise_for_status()
                dados_cliente = res_det.json()

                st.write(f"Nome: {dados_cliente['nome']}")
                st.write(f"Telefone: {dados_cliente['telefone']}")
                st.write(f"Nascimento: {formatar_data_br(dados_cliente['nascimento'])}")
                st.write(f"Hora Agendada: {dados_cliente['hora_agendada']}")
                st.write(f"Instagram: {dados_cliente['instagram']}")
                st.write(f"Cantor favorito: {dados_cliente['cantor']}")
                st.write(f"Bebida favorita: {dados_cliente['bebida']}")
                st.write(f"Já fez epilação na cera? {dados_cliente['epilacao']}")
                st.write(f"Possui alergia? {dados_cliente['alergia']}")
                if dados_cliente['alergia'] == "SIM":
                    st.write(f"Qual alergia? {dados_cliente['qual_alergia']}")
                st.write(f"Problemas de pele? {dados_cliente['problemas_pele']}")
                st.write(f"Tratamento dermatológico? {dados_cliente['tratamento']}")
                st.write(f"Tipo de pele: {dados_cliente['tipo_pele']}")
                st.write(f"Hidrata a pele? {dados_cliente['hidrata']}")
                st.write(f"Está grávida? {dados_cliente['gravida']}")
                st.write(f"Uso de medicamentos? {dados_cliente['medicamento']}")
                if dados_cliente['medicamento'] == "SIM":
                    st.write(f"Qual medicamento? {dados_cliente['qual_medicamento']}")
                st.write(f"DIU ou marca-passo? {dados_cliente['uso']}")
                st.write(f"Diabetes? {dados_cliente['diabete']}")
                st.write(f"Pelos encravados? {dados_cliente['pelos_encravados']}")
                st.write(f"Cirurgia recente? {dados_cliente['cirurgia']}")
                st.write(f"Foliculite? {dados_cliente['foliculite']}")
                if dados_cliente['foliculite'] == "SIM":
                    st.write(f"Qual foliculite? {dados_cliente['qual_foliculite']}")
                st.write(f"Outro problema? {dados_cliente['problema_extra']}")
                if dados_cliente['problema_extra'] == "SIM":
                    st.write(f"Qual problema? {dados_cliente['qual_problema']}")
                st.write(f"Autoriza uso de imagem? {dados_cliente['autorizacao_imagem']}")

                if dados_cliente.get("assinatura"):
                    assinatura_bytes = base64.b64decode(dados_cliente["assinatura"])
                    st.image(assinatura_bytes, caption="Assinatura digital", use_column_width=True)

                if st.button("Excluir Cliente"):
                    try:
                        res_del = requests.delete(f"{API_URL}/clientes/{cliente_id}")
                        res_del.raise_for_status()
                        st.success("Cliente excluído com sucesso!")
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f"Erro ao excluir cliente: {e}")

            except Exception as e:
                st.error(f"Erro ao buscar detalhes do cliente: {e}")

