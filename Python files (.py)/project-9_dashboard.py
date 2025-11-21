from lightningchart_trader import TAChart
import pandas as pd
import os
import requests 
license_key_path = "Python-Trader_License_key.txt" 
# license key for python trader and the stock API
license_key = open(license_key_path).read()
api_key_path = "API-key.txt"
api_key = open(api_key_path).read() 
filepath = 'data/project-9/'
company_names = []
# Get file names
csv_list = os.listdir(filepath)
# Trader instance initialization
trader = TAChart(license_key)
# Using Alphavantages ticker search api get the names of companies analyzed.
for stock in csv_list:
    stock_ticker = stock.replace('.csv','')
    api_url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={stock_ticker}&apikey={api_key}'
    request = requests.get(api_url).json()
    stock_name = request['bestMatches'][0]['2. name']
    company_names.append(stock_name)

# Create a dashboard with two columns and 5 rows. The row and column index determine the charts position wihtin the dashboard.
dashboard = trader.create_dashboard(5, 2)
row_index = 0
column_index = 0
use_adjusted = False

# Loop used to import data to the trader.
for index, (name, company) in enumerate(zip(company_names, csv_list)):
    row_index = index // 2
    column_index = index % 2
    stock_dataframe = pd.read_csv(filepath + company)
    newchart = dashboard.add_chart('Line', row_index, column_index, title=name).set_data(stock_dataframe)
    newchart.add_volume()
trader.open()