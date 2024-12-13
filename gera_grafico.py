import subprocess
import sys

# Function to install packages
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# List of required packages
required_packages = ["pandas", "openpyxl", "matplotlib", "PyMuPDF"]

# Install required packages
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        install(package)

# Import libraries after installation
import pandas as pd
import matplotlib.pyplot as plt
import openpyxl
from openpyxl.drawing.image import Image
import fitz

# Function to extract text from a PDF and return a list
def extract_text_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

# Function to process the extracted text and get the types
def get_types_from_text(text):
    lines = text.split('\n')
    types = []
    for line in lines:
        if 'TIPO' in line or line.strip() == '':
            continue
        tipo = line.split(":")[0].strip()
        types.append(tipo)
    return types

# Extract text from the PDF
pdf_path = 'funds_data.pdf'  # Path to the PDF file
text = extract_text_from_pdf(pdf_path)

# Get the types from the extracted text
data = get_types_from_text(text)

# Create a DataFrame with the data
df = pd.DataFrame(data, columns=["Type"])

# Count the frequency of each item
frequency = df["Type"].value_counts()

# Export the frequency data to an Excel file
frequency_df = frequency.reset_index()
frequency_df.columns = ["Type", "Frequency"]
frequency_df.to_excel("frequency_funds.xlsx", index=False)

# Create a bar chart
plt.figure(figsize=(10, 8))
frequency.plot(kind="bar")
plt.title("Frequency of Fund Types")
plt.xlabel("Fund Type")
plt.ylabel("Frequency")
plt.xticks(rotation=90)
plt.tight_layout()

# Save the chart to the Excel file
with pd.ExcelWriter("frequency_funds.xlsx", engine="openpyxl", mode="a") as writer:
    frequency_df.to_excel(writer, sheet_name="Frequency", index=False)
    workbook = writer.book
    worksheet = workbook.create_sheet("Chart")
    img_data = plt.gcf()
    img_data.savefig("frequency_chart.png")
    img = Image("frequency_chart.png")
    worksheet.add_image(img, "A1")

# Display the chart
plt.show()

print("Data and chart exported to 'frequency_funds.xlsx'.")
