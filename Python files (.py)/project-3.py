import requests
from lightningchart_trader import TAChart
license_key_path = "Python-Trader_License_key.txt" 
# Load the license key and initializing Python trader
license_key = open(license_key_path).read()
trader = TAChart(license_key)
# api_name is the APi you wish to use for data eg: TIME_SERIES_DAILY. 'ticker' is the ticker specific stock eg: AAPL 
# key is your Alphavantage API key
# https://www.alphavantage.co/query?function=api_name&symbol=ticker&apikey=key
api_key_path = "API-key.txt" 
# Load the license key 
key = open(api_key_path).read() 


def get_data(api_name: str, data_interval: str):
    """Make an API call using the following parameters """
    # API call url, recieved as JSON then converted to a Python dictionary
    call_url = f'https://www.alphavantage.co/query?function={api_name}&interval={data_interval}&apikey={key}'
    api_response = requests.get(call_url).json()
    print(api_response)
    # Parsing the data from the API
    data_list = []
    for entry in api_response['data']:
      date = entry['date']
      # Some entries are empty thus should not be processed. 
      if entry['value'] != '.': 
         price_data = float(entry['value'])
         # Python trader requires open,high,low,close and a date to work properly. 
         # The commodities API doesn't return all of them only single price value and a date
         # This can be circumvented, just remember that some charts/indicators won't work
         # Add the new dictionary to a list
         data_list.append({'open': price_data, 
                           'high': price_data,
                           'low': price_data,
                           'close': price_data, 
                           'date':date})
    trader.set_chart_title(f'{api_response['name']} data {data_interval}')
    # Import the list of dictionaries to Python Trader
    trader.set_data(data_list)


def open_chart1():
    """GDP data"""

    get_data('REAL_GDP', 'quarterly')
    trader.set_color_theme('darkGold')
    trader.set_line_color("#B69E00")
    trader.set_price_chart_type('Mountain')
    trader.open()


def open_chart2():
    """GDP data"""

    get_data('REAL_GDP', 'annual')
    trader.set_color_theme('darkGold')
    trader.set_line_color("#B69E00")
    trader.set_price_chart_type('Mountain')
    trader.open()


def open_chart3():
    """GDP per capita"""

    get_data('REAL_GDP_PER_CAPITA', 'quarterly')
    trader.set_color_theme('turquoiseHexagon')
    trader.set_line_color("#0EE936")
    trader.set_price_chart_type('Line')
    trader.open()


def open_chart4():
    """historical inflation"""
    
    get_data('INFLATION', 'quarterly')
    trader.set_color_theme('turquoiseHexagon')
    trader.set_line_color("#E92F0E")
    trader.set_price_chart_type('Line')
    trader.open()


def open_chart5():
    """GDP per capita"""
    
    get_data('UNEMPLOYMENT', 'quarterly')
    trader.set_color_theme('darkGold')
    trader.set_line_color("#00CE6B")
    trader.set_price_chart_type('Line')
    trader.open()


#Change the name to whichever chart you wish to open
open_chart5()
   
    


