import pandas as pd
import os
from lightningchart_trader import TAChart
license_key_path = "Python-Trader_License_key.txt" 
# Load the license key and initializing Python trader
license_key = open(license_key_path).read()
# api_name is the APi you wish to use for data eg: TIME_SERIES_DAILY. 'ticker' is the ticker specific stock eg: AAPL 
# key is your Alphavantage API key
# https://www.alphavantage.co/query?function=api_name&symbol=ticker&apikey=key
api_key_path = "API-key.txt" 
# Load the license key 
api_key = open(api_key_path).read()

filepath = 'data/project-7/'
stocks = os.listdir(filepath)
company_names = [
        'Agilent Technologies, Inc.',
        'Steelcase Inc.',
        'West Pharmaceutical Services, Inc.'    
        ]

for company_data, title in zip(stocks, company_names):
    """Method used to import data to the trader. Optionally you can set chart properties here."""

    # The filepath might have to be adjusted
    # Python Trader can work with pandas dataframes, assuming all the relevant variables are present. 
    # What this means in practise is that the columns are labelled afetr the required data fields. (open,high,low,close,date)
    stock_dataframe = pd.read_csv(filepath + company_data)
    # Initialize the trader software with your license key and set dataframe as the data.
    trader = TAChart(license_key)
    trader.set_data(stock_dataframe)
    # Chart customization. Optional and can also be done in UI, but this way makes it more convenient.
    trader.set_color_theme('cyberSpace')
    trader.set_positive_body_color("#0b6a09")
    trader.set_positive_wick_color("#0aee24")
    trader.set_negative_body_color("#8a0606")
    trader.set_negative_wick_color("#fe0101")
    trader.add_volume(False,False)
    trader.set_chart_title(title)
    trader.open()




