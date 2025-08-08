from datetime import datetime

def formatar_data_br(data_iso):
    """
    Formata uma data no formato ISO (yyyy-mm-dd) para o formato brasileiro dd/mm/yyyy.
    """
    try:
        return datetime.strptime(data_iso, "%Y-%m-%d").strftime("%d/%m/%Y")
    except Exception:
        return data_iso

def formatar_moeda(valor):
    """
    Formata um valor numérico como moeda brasileira (R$ 0,00).
    """
    try:
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return valor

def validar_email(email):
    """
    Validação simples de email (exemplo básico).
    """
    import re
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(padrao, email) is not None

def limpar_formulario(session_keys):
    """
    Limpa variáveis do estado da sessão passadas como lista.
    """
    for key in session_keys:
        if key in st.session_state:
            del st.session_state[key]

