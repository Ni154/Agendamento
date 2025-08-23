import os
import requests

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

def send_email_resend(to_email, subject, html_content):
    """
    Envia um e-mail usando a API do Resend
    """
    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "from": "Seu App <no-reply@seuapp.com>",  # Pode alterar para seu domínio se quiser
        "to": [to_email],
        "subject": subject,
        "html": html_content
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        print(f"Erro ao enviar e-mail: {response.text}")
    else:
        print(f"E-mail enviado para {to_email} com sucesso!")
    return response
