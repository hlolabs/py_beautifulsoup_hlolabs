import subprocess
import sys
import urllib.request
from bs4 import BeautifulSoup
import csv
from fpdf import FPDF  

# URL da página que você deseja acessar
url = "https://www.fundsexplorer.com.br/funds"

# Configurando o cabeçalho User-Agent
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

# Fazendo a requisição da página
req = urllib.request.Request(url, headers=headers)

with urllib.request.urlopen(req) as response:
    page = response.read()

# Fazendo o parsing do HTML
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
        
        # Capturando valores de DY e PL
        dy = info_boxes[0].text.strip() if len(info_boxes) > 0 else ""
        pl = info_boxes[1].text.strip() if len(info_boxes) > 1 else ""
        
        # Adicionando os dados na lista
        data.append([tipo, nome, dy, pl])

# Escrevendo os dados em um arquivo CSV com codificação correta
with open('./funds_data.csv', 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(['TIPO', 'NOME', 'DY(%)', 'PL(R$)'])  # Cabeçalho
    writer.writerows(data)

print("Dados exportados para 'funds_data.csv'.")

# Criando um arquivo CSV somente com os nomes
with open('./funds_names.csv', 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(['NOME'])  # Cabeçalho
    for row in data:
        writer.writerow([row[1]])  # Apenas a coluna 'NOME'

print("Nomes exportados para 'funds_names.csv'.")

# Função para exportar dados do CSV para PDF
def export_csv_to_pdf(csv_file, pdf_filename):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Configurando a fonte
    pdf.set_font("Arial", size=12)
    
    # Abrindo o CSV
    with open(csv_file, mode='r', encoding='utf-8-sig') as file:
        reader = csv.reader(file, delimiter=',')
        
        # Processando cada linha do CSV
        for row in reader:
            # Formatando a linha com vírgulas
            line = ', '.join(row)
            
            # Adicionando cada linha ao PDF
            pdf.cell(200, 10, txt=line, ln=True)
    
    # Salvando o PDF
    pdf.output(pdf_filename)

# Exportando dados do CSV para PDF
csv_file = './funds_data.csv'
pdf_filename = './funds_data.pdf'
export_csv_to_pdf(csv_file, pdf_filename)

print(f"Dados do CSV exportados para PDF como '{pdf_filename}'.")
