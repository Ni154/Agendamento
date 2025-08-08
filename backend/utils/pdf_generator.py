from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from io import BytesIO

def gerar_pdf_venda(cliente_nome: str, data: str, itens: list, total: float) -> bytes:
    """
    Gera um PDF da venda com dados do cliente, data, itens (lista de dicts) e total.
    Retorna o PDF em bytes para enviar, salvar ou exibir.
    
    itens: [{'nome': str, 'quantidade': int, 'preco': float}, ...]
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    largura, altura = A4

    c.setFont("Helvetica-Bold", 14)
    c.drawString(2*cm, altura - 2*cm, f"Venda - Cliente: {cliente_nome}")
    c.setFont("Helvetica", 12)
    c.drawString(2*cm, altura - 3*cm, f"Data: {data}")

    y = altura - 4*cm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2*cm, y, "Item")
    c.drawString(10*cm, y, "Qtd")
    c.drawString(13*cm, y, "Preço Unit.")
    c.drawString(17*cm, y, "Total")
    y -= 0.5*cm
    c.line(2*cm, y, 19*cm, y)
    y -= 0.5*cm

    c.setFont("Helvetica", 12)
    for item in itens:
        nome = item['nome']
        qtd = item['quantidade']
        preco = item['preco']
        total_item = qtd * preco
        c.drawString(2*cm, y, nome)
        c.drawString(10*cm, y, str(qtd))
        c.drawString(13*cm, y, f"R$ {preco:.2f}")
        c.drawString(17*cm, y, f"R$ {total_item:.2f}")
        y -= 0.5*cm
        if y < 3*cm:  # Nova página se espaço acabar
            c.showPage()
            y = altura - 2*cm

    y -= 0.5*cm
    c.line(2*cm, y, 19*cm, y)
    y -= 1*cm
    c.setFont("Helvetica-Bold", 14)
    c.drawString(13*cm, y, f"Total: R$ {total:.2f}")

    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf

