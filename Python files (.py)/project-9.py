from lightningchart_trader import TAChart
import pandas as pd
import os
import requests
license_key_path = "Python-Trader_License_key.txt" 
# Load the license key and initializing Python trader
license_key = open(license_key_path).read()
api_key_path = "API-key.txt" 
# Load the license key 
api_key = open(api_key_path).read() 
filepath = 'data/project-9/'
company_names = []
# Get file names
csv_list = os.listdir(filepath)
print(csv_list)
# Trader instance initialization
trader = TAChart(license_key)

# Using Alphavantages ticker search api get the names of companies analyzed.
for stock in csv_list:
    stock_ticker = stock.replace('.csv','')
    api_url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={stock_ticker}&apikey={api_key}'
    request = requests.get(api_url).json()
    print(request)
    stock_name = request['bestMatches'][0]['2. name']
    company_names.append(stock_name)

# Index used to access individual files in the csv_list
# Note the index value might vary if the files are in different order, compared to the example
file_index = 2
stock_dataframe = pd.read_csv(filepath + csv_list[file_index])
# Python trader requires the fields Open,Low,High,Close to function properly. The fields name are case sensitive.
# Add a volume indicator
trader.add_volume()
trader.change_time_range(3)
trader.set_color_theme('darkGold')
trader.set_data(stock_dataframe)
trader.set_chart_title(company_names[file_index])
trader.open()