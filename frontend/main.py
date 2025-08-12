import streamlit as st
import requests

# Ajuste aqui a URL da sua API backend (FastAPI)
API_URL = "https://seu-backend-url.railway.app"

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
        resp = requests.post(f"{API_URL}/auth/login", json={"usuario": usuario, "senha": senha})
        if resp.status_code == 200:
            return resp.json().get("access_token")
        else:
            st.error(f"Erro no login: {resp.json().get('detail')}")
            return None
    except Exception as e:
        st.error(f"Erro na conexão: {e}")
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

# --- TELA LOGIN ---
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
        else:
            st.error("Usuário ou senha inválidos")

# --- TELA INÍCIO ---
def tela_inicio():
    st.subheader("👋 Seja bem-vindo(a)!")
    st.write("Use o menu lateral para navegar pelas funcionalidades.")

# --- TELA DASHBOARD ---
def tela_dashboard():
    st.subheader("📊 Dashboard")
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        resp = requests.get(f"{API_URL}/dashboard", headers=headers)
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
    except Exception as e:
        st.error(f"Erro: {e}")

# --- ROTEAMENTO DE TELAS ---
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
        elif menu == "Cadastro Cliente":
            st.subheader("🧍 Cadastro Cliente")
            st.info("Aqui vai o componente de cadastro cliente")
        elif menu == "Cadastro Empresa":
            st.subheader("🏢 Cadastro Empresa")
            st.info("Aqui vai o componente de cadastro empresa")
        elif menu == "Cadastro Produtos":
            st.subheader("📦 Cadastro Produtos")
            st.info("Aqui vai o componente de cadastro produtos")
        elif menu == "Cadastro Serviços":
            st.subheader("💆 Cadastro Serviços")
            st.info("Aqui vai o componente de cadastro serviços")
        elif menu == "Agendamento":
            st.subheader("📅 Agendamento")
            st.info("Aqui vai o componente de agendamento")
        elif menu == "Vendas":
            st.subheader("💰 Vendas")
            st.info("Aqui vai o componente de vendas")
        elif menu == "Cancelar Vendas":
            st.subheader("🚫 Cancelar Vendas")
            st.info("Aqui vai o componente para cancelar vendas")
        elif menu == "Despesas":
            st.subheader("💸 Despesas")
            st.info("Aqui vai o componente de despesas")
        elif menu == "Relatórios":
            st.subheader("📈 Relatórios")
            st.info("Aqui vai o componente de relatórios")
        elif menu == "Backup":
            st.subheader("💾 Backup")
            st.info("Aqui vai o componente de backup")
        else:
            st.write("Menu não implementado ainda")

if __name__ == "__main__":
    main()
