import streamlit as st
import requests

API_URL = "http://localhost:8000"  # Ajuste para o URL real da sua API backend

# Inicializa estado de login
if "login" not in st.session_state:
    st.session_state.login = False
if "token" not in st.session_state:
    st.session_state.token = None
if "menu" not in st.session_state:
    st.session_state.menu = None

def login_api(usuario, senha):
    # Exemplo simples de login (ajuste conforme sua API)
    try:
        response = requests.post(f"{API_URL}/auth/login", json={"usuario": usuario, "senha": senha})
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            return None
    except Exception:
        return None

def logout():
    st.session_state.login = False
    st.session_state.token = None
    st.session_state.menu = None

def menu_options():
    return [
        "Início", "Dashboard", "Cadastro Cliente", "Cadastro Empresa",
        "Cadastro Produtos", "Cadastro Serviços", "Agendamento",
        "Vendas", "Cancelar Vendas", "Despesas", "Relatórios", "Backup", "Sair"
    ]

def render_menu():
    icones_menu = {
        "Início": "🏠",
        "Dashboard": "📊",
        "Cadastro Cliente": "🧍",
        "Cadastro Empresa": "🏢",
        "Cadastro Produtos": "📦",
        "Cadastro Serviços": "💆",
        "Agendamento": "📅",
        "Vendas": "💰",
        "Cancelar Vendas": "🚫",
        "Despesas": "💸",
        "Relatórios": "📈",
        "Backup": "💾",
        "Sair": "🔓"
    }
    with st.sidebar:
        st.title("Menu")
        for opcao in menu_options():
            icone = icones_menu.get(opcao, "📌")
            if st.button(f"{icone} {opcao}"):
                if opcao == "Sair":
                    logout()
                else:
                    st.session_state.menu = opcao

def main():
    st.set_page_config(page_title="Studio Depilação", layout="wide")

    if not st.session_state.login:
        st.title("🔐 Login")
        usuario_input = st.text_input("Usuário")
        senha_input = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            token = login_api(usuario_input, senha_input)
            if token:
                st.session_state.login = True
                st.session_state.token = token
                st.experimental_rerun()
            else:
                st.error("Usuário ou senha inválidos")
    else:
        render_menu()

        menu = st.session_state.menu or "Início"
        st.title(f"🧭 {menu}")

        # Exemplo de renderização por menu
        if menu == "Início":
            st.subheader("👋 Seja bem-vindo(a)!")
            # Aqui você pode colocar a tela inicial (ex: resumo, agendamentos do dia etc.)

        elif menu == "Dashboard":
            st.subheader("📊 Dashboard")
            # Chamadas API e exibição dados do dashboard

        elif menu == "Cadastro Cliente":
            st.subheader("🧍 Cadastro Cliente")
            # Importar componente frontend para cadastro cliente

        # TODO: Adicione os demais menus conforme necessidade, importando seus componentes ou funções

if __name__ == "__main__":
    main()

