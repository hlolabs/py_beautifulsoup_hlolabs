# py_beautifulsoup

# Projeto de Coleta e Análise de Dados de Fundos Imobiliários

## Descrição

Este projeto foi desenvolvido para coletar dados de fundos imobiliários a partir do site [Funds Explorer](https://www.fundsexplorer.com.br/funds), processar as informações e exportá-las para um arquivo CSV. O objetivo é permitir a análise das informações coletadas, incluindo o tipo de fundo, nome, Dividend Yield (DY) e Preço sobre Lucro (PL) de cada fundo listado na página.

## Funcionalidades

- Coleta de dados de fundos imobiliários a partir de uma página web.
- Processamento e extração de informações relevantes.
- Exportação dos dados coletados para um arquivo CSV.

## Pré-requisitos

Para executar este projeto, é necessário ter o Python instalado em seu ambiente. Além disso, o projeto utiliza algumas bibliotecas específicas, que serão instaladas automaticamente pelo próprio código, se necessário.

## Bibliotecas Utilizadas

- **urllib.request**: Utilizada para realizar requisições HTTP e acessar o conteúdo da página web.
- **beautifulsoup4**: Utilizada para fazer o parse do HTML e extrair as informações desejadas da página.
- **csv**: Utilizada para escrever os dados processados em um arquivo CSV.

## Como Executar o Projeto

1. **Clone o repositório:**

    ```bash
    git clone https://github.com/seu-usuario/nome-do-repositorio.git
    cd nome-do-repositorio
    ```

2. **Execute o código Python:**

    ```bash
    python main.py
    ```

3. **Verifique o arquivo CSV gerado:**

    O arquivo `funds_data.csv` será gerado na pasta do projeto, contendo os dados coletados e processados.

## Detalhes do Código

O código realiza as seguintes etapas:

1. **Instalação de dependências**: Verifica se as bibliotecas necessárias (`beautifulsoup4`) estão instaladas e as instala automaticamente, se necessário.

    ```python
    def install(package):
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    required_packages = ["beautifulsoup4"]
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            install(package)
    ```

2. **Importação de bibliotecas**: Importa as bibliotecas necessárias para o funcionamento do código.

    ```python
    import urllib.request
    from bs4 import BeautifulSoup
    import csv
    ```

3. **Requisição da página**: Configura o cabeçalho User-Agent e faz a requisição da página web.

    ```python
    url = "https://www.fundsexplorer.com.br/funds"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    req = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(req) as response:
        page = response.read()
    ```

4. **Parse do HTML**: Utiliza o BeautifulSoup para fazer o parse do HTML e encontrar os itens desejados.

    ```python
    soup = BeautifulSoup(page, 'html.parser')
    tickers = soup.find_all('div', class_='tickerBox')
    ```

5. **Coleta de dados**: Extrai as informações relevantes (tipo, nome, DY, PL) de cada fundo imobiliário e armazena em uma lista.

    ```python
    data = []

    for ticker in tickers:
        type_span = ticker.find('span', class_='tickerBox__type')
        title_div = ticker.find('div', attrs={'data-element': 'ticker-box-title'})
        info_boxes = ticker.find_all('div', class_='tickerBox__info__box')

        if type_span and title_div:
            tipo = type_span.text.strip()
            nome = title_div.text.strip()
            dy = info_boxes[0].text.strip() if len(info_boxes) > 0 else ""
            pl = info_boxes[1].text.strip() if len(info_boxes) > 1 else ""
            data.append([tipo, nome, dy, pl])
    ```

6. **Exportação para CSV**: Escreve os dados coletados em um arquivo CSV com codificação UTF-8.

    ```python
    with open('./funds_data.csv', 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(['TIPO', 'NOME', 'DY(%)', 'PL(R$)'])
        writer.writerows(data)
    ```

7. **Mensagem de sucesso**: Exibe uma mensagem informando que os dados foram exportados com sucesso.

    ```python
    print("Dados exportados para 'funds_data.csv'.")
    ```

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
