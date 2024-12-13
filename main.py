import subprocess
import sys

# Função para instalar pacotes
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Lista de pacotes necessários
required_packages = ["requests", "beautifulsoup4", "pandas", "openpyxl"]

# Instalar pacotes necessários
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        install(package)

# Importação de bibliotecas após instalação
import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL da página com a lista de FIIs
url = "https://www.fundsexplorer.com.br/funds"

# Requisição para a página
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Listas para armazenar os dados
tickers = []
setores = []

# Encontrando todos os spans que contêm as informações
spans = soup.find_all('span', class_='tickerBox__type')

for span in spans:
    texto = span.text.strip()
    if ':' in texto:
        ticker, setor = texto.split(':', 1)
        tickers.append(ticker.strip())
        setores.append(setor.strip())

# Criando um DataFrame e exportando para Excel
df = pd.DataFrame({'Ticker': tickers, 'Setor': setores})
df.to_excel('lista_fiis.xlsx', index=False)

print("Lista de FIIs com setores salva em 'lista_fiis.xlsx'")
