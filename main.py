import subprocess
import sys

# Função para instalar pacotes
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Lista de pacotes necessários
required_packages = ["beautifulsoup4"]

# Instalar pacotes necessários
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        install(package)

# Importação de bibliotecas após instalação
import urllib.request
from bs4 import BeautifulSoup
import csv

# URL da página que você deseja acessar
url = "https://www.fundsexplorer.com.br/funds"

# Configurando o cabeçalho User-Agent
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

# Fazendo a requisição da página
req = urllib.request.Request(url, headers=headers)

with urllib.request.urlopen(req) as response:
    page = response.read()

# Parseando o HTML
soup = BeautifulSoup(page, 'html.parser')

# Encontrando todos os itens desejados
tickers = soup.find_all('div', class_='tickerBox')

# Lista para armazenar os dados
data = []

# Coletando os dados
for ticker in tickers:
    type_span = ticker.find('span', class_='tickerBox__type')
    title_div = ticker.find('div', attrs={'data-element': 'ticker-box-title'})
    info_boxes = ticker.find_all('div', class_='tickerBox__info__box')

    if type_span and title_div:
        tipo = type_span.text.strip()
        nome = title_div.text.strip()
        
        # Capturando os valores de DY e PL
        dy = info_boxes[0].text.strip() if len(info_boxes) > 0 else ""
        pl = info_boxes[1].text.strip() if len(info_boxes) > 1 else ""
        
        # Adicionando dados à lista
        data.append([tipo, nome, dy, pl])

# Escrevendo os dados em um arquivo CSV com codificação correta
with open('funds_data.csv', 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(['TIPO', 'NOME', 'DY(%)', 'PL(R$)'])  # Cabeçalho
    writer.writerows(data)

print("Dados exportados para 'funds_data.csv'.")
