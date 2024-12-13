import subprocess
import sys

# Function to install packages
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# List of required packages
required_packages = ["beautifulsoup4"]

# Install required packages
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        install(package)

# Import libraries after installation
import urllib.request
from bs4 import BeautifulSoup
import csv

# URL of the page you want to access
url = "https://www.fundsexplorer.com.br/funds"

# Configuring the User-Agent header
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

# Making the page request
req = urllib.request.Request(url, headers=headers)

with urllib.request.urlopen(req) as response:
    page = response.read()

# Parsing the HTML
soup = BeautifulSoup(page, 'html.parser')

# Finding all desired items
tickers = soup.find_all('div', class_='tickerBox')

# List to store the data
data = []

# Collecting the data
for ticker in tickers:
    type_span = ticker.find('span', class_='tickerBox__type')
    title_div = ticker.find('div', attrs={'data-element': 'ticker-box-title'})
    info_boxes = ticker.find_all('div', class_='tickerBox__info__box')

    if type_span and title_div:
        tipo = type_span.text.strip()
        nome = title_div.text.strip()
        
        # Capturing DY and PL values
        dy = info_boxes[0].text.strip() if len(info_boxes) > 0 else ""
        pl = info_boxes[1].text.strip() if len(info_boxes) > 1 else ""
        
        # Adding data to the list
        data.append([tipo, nome, dy, pl])

# Writing the data to a CSV file with correct encoding
with open('./funds_data.csv', 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    writer.writerow(['TIPO', 'NOME', 'DY(%)', 'PL(R$)'])  # Header
    writer.writerows(data)

print("Data exported to 'funds_data.csv'.")
