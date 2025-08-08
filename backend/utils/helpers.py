from datetime import datetime

def formatar_data_br(data_iso: str) -> str:
    """
    Converte data no formato ISO (YYYY-MM-DD) para formato brasileiro (DD/MM/YYYY).
    """
    try:
        return datetime.strptime(data_iso, "%Y-%m-%d").strftime("%d/%m/%Y")
    except Exception:
        return data_iso

def calcular_total_itens(itens: list) -> float:
    """
    Calcula o total somando (quantidade * preco) de cada item da lista.
    Espera lista de dicts: [{'quantidade': int, 'preco': float}, ...]
    """
    total = 0.0
    for item in itens:
        total += item.get('quantidade', 0) * item.get('preco', 0)
    return total

def validar_email(email: str) -> bool:
    """
    Valida email simples.
    """
    import re
    padrao = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(padrao, email) is not None

