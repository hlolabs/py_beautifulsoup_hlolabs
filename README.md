# py_beautifulsoup_hlolabs
# Real Estate Funds Data Collection and Analysis Project

## Description

This project was developed to collect real estate funds data from the [Funds Explorer](https://www.fundsexplorer.com.br/funds) website, process the information, and export it to a CSV file. The goal is to allow the analysis of the collected information, including the type of fund, name, Dividend Yield (DY), and Price-to-Earnings (PL) of each fund listed on the page.

## Features

- Data collection of real estate funds from a web page.
- Processing and extraction of relevant information.
- Exporting the collected data to a CSV file.

## Prerequisites

To run this project, you need to have Python installed in your environment. Additionally, the project uses some specific libraries that will be automatically installed by the code if necessary.

## Libraries Used

- **urllib.request**: Used to make HTTP requests and access the web page content.
- **beautifulsoup4**: Used to parse HTML and extract the desired information from the page.
- **csv**: Used to write the processed data to a CSV file.

## How to Run the Project

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/repository-name.git
    cd repository-name
    ```

2. **Run the Python code:**

    ```bash
    python main.py
    ```

3. **Check the generated CSV file:**

    The `funds_data.csv` file will be generated in the project folder, containing the collected and processed data.

## Code Details

The code performs the following steps:

1. **Dependency installation**: Checks if the necessary libraries (`beautifulsoup4`) are installed and installs them automatically if needed.

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

2. **Importing libraries**: Imports the libraries required for the code to function.

    ```python
    import urllib.request
    from bs4 import BeautifulSoup
    import csv
    ```

3. **Page request**: Configures the User-Agent header and makes the web page request.

    ```python
    url = "https://www.fundsexplorer.com.br/funds"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    req = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(req) as response:
        page = response.read()
    ```

4. **HTML parsing**: Uses BeautifulSoup to parse the HTML and find the desired items.

    ```python
    soup = BeautifulSoup(page, 'html.parser')
    tickers = soup.find_all('div', class_='tickerBox')
    ```

5. **Data collection**: Extracts relevant information (type, name, DY, PL) for each real estate fund and stores it in a list.

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

6. **Export to CSV**: Writes the collected data to a CSV file with UTF-8 encoding.

    ```python
    with open('./funds_data.csv', 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(['TYPE', 'NAME', 'DY(%)', 'PL(R$)'])
        writer.writerows(data)
    ```

7. **Success message**: Displays a message informing that the data has been successfully exported.

    ```python
    print("Data exported to 'funds_data.csv'.")
    ```

## Contributions

Contributions are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License.

