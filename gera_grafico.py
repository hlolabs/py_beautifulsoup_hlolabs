import pandas as pd
import openpyxl
from openpyxl.chart import BarChart, Reference
import csv

# Read the CSV data
csv_file = 'funds_data.csv'

# Read the CSV file with correct encoding and delimiter (semicolon in your example)
csv_data = pd.read_csv(csv_file, delimiter=',', encoding='utf-8-sig')

# Split the 'TIPO' column into two new columns: 'TIPO_CATEGORY' and 'TIPO_DESCRIPTION'
csv_data[['TIPO_CATEGORY', 'TIPO_DESCRIPTION']] = csv_data['TIPO'].str.split(':', expand=True)

# Count the frequency of each 'TIPO_CATEGORY'
frequency = csv_data['TIPO_CATEGORY'].value_counts()

# Create a DataFrame from the frequency count
frequency_df = frequency.reset_index()
frequency_df.columns = ["Type", "Frequency"]

# Export the frequency data to an Excel file and add the chart
with pd.ExcelWriter("frequency_funds.xlsx", engine="openpyxl") as writer:
    # Write frequency data to the 'Frequency' sheet
    frequency_df.to_excel(writer, sheet_name="Frequency", index=False)
    workbook = writer.book
    worksheet = workbook["Frequency"]

    # Create the chart
    chart = BarChart()
    chart.type = "col"
    chart.style = 10
    chart.title = "Frequency of Fund Types"
    chart.x_axis.title = "Fund Type"
    chart.y_axis.title = "Frequency"
    
    # Define data for the chart
    data = Reference(worksheet, min_col=2, min_row=1, max_col=2, max_row=len(frequency_df) + 1)
    categories = Reference(worksheet, min_col=1, min_row=2, max_row=len(frequency_df) + 1)
    
    # Add data to the chart
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(categories)

    # Position the chart in the worksheet
    worksheet.add_chart(chart, "E5")

    # Create a second sheet for all items ordered by 'TIPO'
    sorted_data = csv_data.sort_values(by='TIPO_CATEGORY')

    # Write the sorted data to the 'All Funds Sorted' sheet
    sorted_data.to_excel(writer, sheet_name="All Funds Sorted", index=False)

    print("Data, chart, and grouped data exported to 'frequency_funds.xlsx'.")
