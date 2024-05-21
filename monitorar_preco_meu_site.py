import requests
from bs4 import BeautifulSoup
import smtplib
import time
import locale
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
load_dotenv()

url_produto = "http://localhost:3000/"
preco_desejado = 500.00

email = os.getenv('EMAIL')
senha = os.getenv('PASSWORD')
smtp_server = 'smtp.office365.com'
port = 587

def enviar_email():
    assunto = "Preço do Produto Atingiu o Valor Desejado!"
    corpo = f"O preço do produto atingiu o valor de R${preco_desejado}. Acesse o link: {url_produto}"

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = email
    msg['Subject'] = assunto
    msg.attach(MIMEText(corpo, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(email, senha)
        server.sendmail(email, email, msg.as_string())
        server.quit()
        print('E-mail enviado com sucesso!')
    except Exception as e:
        print('Erro ao enviar o e-mail:', e)

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def monitorar_preco():
    while True:
        resposta = requests.get(url_produto)
        soup = BeautifulSoup(resposta.text, 'html.parser')
        elemento_preco = soup.find('h4', {'class': 'finalPrice'})

        if elemento_preco is None:
            print("Elemento de preço não encontrado.")
            time.sleep(1)
            continue

        preco_str = elemento_preco.text.replace('R$', '').replace('.', '').replace(',', '').replace('\xa0', '').strip()
        preco_atual = float(preco_str) / 100

        preco_formatado = locale.currency(preco_atual, grouping=True, symbol=None).replace('R$', 'R$ ')

        if preco_atual <= preco_desejado:
            enviar_email()
            break

        print(f"Preço atual: {preco_formatado}")
        time.sleep(1)

monitorar_preco()
