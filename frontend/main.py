import streamlit as st
import requests
import os

# URL do backend (pode ser definida como variável de ambiente no Streamlit Cloud)
API_URL = os.getenv("API_URL", "https://agendamento-banco-de-dados.up.railway.app")

# --- SESSION STATE ---
if "login" not in st.session_state:
    st.session_state.login = False
if "token" not in st.session_state:
    st.session_state.token = None
if "menu" not in st.session_state:
    st.session_state.menu = None
if "usuario" not in st.session_state:
    st.session_state.usuario = None

# --- FUNÇÕES API ---
def login_api(usuario, senha):
    try:
        resp = requests.post(
            f"{API_URL}/auth/login",
            json={"usuario": usuario, "senha": senha},
            timeout=10
        )
        if resp.status_code == 200:
            return resp.json().get("access_token")
        else:
            st.error(f"Erro no login: {resp.json().get('detail')}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("Não foi possível conectar ao servidor. Verifique se o backend está online.")
        return None
    except requests.exceptions.Timeout:
        st.error("O servidor demorou muito para responder. Tente novamente.")
        return None
    except Exception as e:
        st.error(f"Erro inesperado: {e}")
        return None

def logout():
    st.session_state.login = False
    st.session_state.token = None
    st.session_state.menu = None
    st.session_state.usuario = None

# --- MENU ---
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
        st.write(f"Usuário: {st.session_state.usuario}")
        for opcao in menu_options():
            icone = icones_menu.get(opcao, "📌")
            if st.button(f"{icone} {opcao}"):
                if opcao == "Sair":
                    logout()
                    st.experimental_rerun()
                else:
                    st.session_state.menu = opcao
                    st.experimental_rerun()

# --- TELAS ---
def tela_login():
    st.title("🔐 Login")
    usuario_input = st.text_input("Usuário")
    senha_input = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        token = login_api(usuario_input, senha_input)
        if token:
            st.session_state.login = True
            st.session_state.token = token
            st.session_state.usuario = usuario_input
            st.experimental_rerun()

def tela_inicio():
    st.subheader("👋 Seja bem-vindo(a)!")
    st.write("Use o menu lateral para navegar pelas funcionalidades.")

def tela_dashboard():
    st.subheader("📊 Dashboard")
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        resp = requests.get(f"{API_URL}/dashboard", headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            st.metric("Clientes", data.get("total_clientes", 0))
            st.metric("Vendas", data.get("total_vendas", 0))
            st.metric("Produtos", data.get("total_produtos", 0))
            st.metric("Serviços", data.get("total_servicos", 0))
            st.metric("Faturamento", f'R$ {data.get("total_faturamento", 0):.2f}')
            st.metric("Despesas", f'R$ {data.get("total_despesas", 0):.2f}')
            st.metric("Lucro Líquido", f'R$ {data.get("lucro_liquido", 0):.2f}')
        else:
            st.error("Erro ao carregar dashboard")
    except requests.exceptions.ConnectionError:
        st.error("Não foi possível conectar ao servidor.")
    except requests.exceptions.Timeout:
        st.error("O servidor demorou muito para responder.")
    except Exception as e:
        st.error(f"Erro: {e}")

# --- MAIN ---
def main():
    st.set_page_config(page_title="Studio Depilação", layout="wide")
    if not st.session_state.login:
        tela_login()
    else:
        render_menu()
        menu = st.session_state.menu or "Início"
        st.title(f"🧭 {menu}")

        if menu == "Início":
            tela_inicio()
        elif menu == "Dashboard":
            tela_dashboard()
        else:
            st.subheader(f"{menu}")
            st.info(f"Aqui vai o componente de {menu.lower()}")

if __name__ == "__main__":
    main()
