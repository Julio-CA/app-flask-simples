from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os

def send_email(email, height, avarege):
    # Configurações do remetente
    remetente = os.getenv('EMAIL_USER')
    senha = os.getenv('EMAIL_PASS')

    # Configurações do destinatário
    destinatario = email
    assunto = "Altura Populacional"
    print(f"\n\nEnviando email para {email} com altura {height}\n\n")
    corpo_plain = "Olá %s! Sua altura é %s 😎. A média de altura da população é %s cm" % (email, height, avarege)
    corpo_html = """
    <html>
    <body>
        <h3 style="color:blue;">Olá! %s</h3>
        <p>Sua altura é <strong>%s</strong> cm😄</p>
        <p>A média de altura da população é <strong>%s</strong> cm</p>
    </body>
    </html>
    """ % (email, height, avarege)

    # Monta o email
    mensagem = MIMEMultipart("alternative")
    mensagem["From"] = remetente
    mensagem["To"] = destinatario
    mensagem["Subject"] = assunto
    mensagem.attach(MIMEText(corpo_plain, "plain"))
    mensagem.attach(MIMEText(corpo_html, "html"))

    # Envia via servidor SMTP do Gmail
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
            servidor.starttls()
            servidor.login(remetente, senha) 
            servidor.send_message(mensagem)
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar: {e}")
