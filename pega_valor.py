import csv
import urllib.request
from bs4 import BeautifulSoup

# Nome dos arquivos CSV e TXT
arquivo_csv = 'funds_data.csv'
arquivo_txt = 'saida.txt'

# URL base
base_url = 'https://www.fundsexplorer.com.br/funds/'

# Função para obter os detalhes do fundo
def obter_detalhes_fundo(nome_fundo):
    url = f'{base_url}{nome_fundo.lower()}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    req = urllib.request.Request(url, headers=headers)
    
    with urllib.request.urlopen(req) as response:
        page = response.read()
    
    soup = BeautifulSoup(page, 'html.parser')
    try:
        # Obtendo o preço
        preco_elemento = soup.find('div', class_='headerTicker__content__price').find('p')
        preco = preco_elemento.text.strip()

        # Obtendo o valor dentro da span
        span_elemento = soup.find('div', class_='headerTicker__content__price').find('span')
        extra_valor = span_elemento.text.strip() if span_elemento else 'N/A'

        return preco, extra_valor
    except Exception as e:
        print(f"Erro ao obter os detalhes para {nome_fundo}: {e}")
        return 'Preço não encontrado', 'N/A'

# Lista para armazenar os resultados
resultados = []

# Adiciona o cabeçalho
resultados.append('NOME, Preço, Variação')

# Exibe mensagem de aguarde
print("Aguarde, processando...")

# Abre o arquivo CSV
with open(arquivo_csv, mode='r', encoding='utf-8') as file:
    # Lê o conteúdo do arquivo CSV
    reader = csv.DictReader(file)
    
    # Itera sobre todas as linhas do CSV
    for row in reader:
        nome_fundo = row['NOME']
        # print(f"Acessando URL: {base_url}{nome_fundo.lower()}")  # Comentado
        preco, extra_valor = obter_detalhes_fundo(nome_fundo)
        resultados.append(f"{nome_fundo}, {preco}, {extra_valor}")
        # print(f"Processed {nome_fundo}: {preco}, {extra_valor}")  # Comentado

# Escreve os resultados no arquivo TXT
with open(arquivo_txt, mode='w', encoding='utf-8') as file:
    for linha in resultados:
        file.write(linha + '\n')

# Exibe mensagem de conclusão
print("Arquivo de saída criado com sucesso!")
