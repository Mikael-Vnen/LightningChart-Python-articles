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

def getData(api_name: str, data_interval: str):
    """Make an API call using the following parameters """

    # APi returns data as JSON thats converted into a Python dictionary
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
         data_list.append({'open': price_data, 'high': price_data,'low': price_data,'close': price_data, 'date':date})
    trader.set_chart_title(f'{api_response['name']} data {data_interval}')
    # Import the list of dictionaries to Python Trader
    trader.set_data(data_list)
    

def oil_chart_one():
    """Crude oil prices at a monthly interval"""

    getData('BRENT', 'monthly')
    trader.set_color_theme('cyberSpace')
    trader.set_line_color("#B69E00")
    trader.set_price_chart_type('Mountain')
    trader.open()


def oil_chart_two():
    """Crude oil prices at a weekly interval"""

    getData('BRENT', 'weekly')
    trader.set_color_theme('cyberSpace')
    trader.set_line_color("#B69E00")
    trader.set_price_chart_type('Mountain')
    trader.open()


def oil_chart_three():
    getData('WTI', 'monthly')
    trader.set_color_theme('cyberSpace')
    trader.set_line_color("#B62A00")
    trader.set_price_chart_type('Line')
    trader.add_standard_deviation()
    trader.add_historical_volatility_index()
    trader.open()


def copper_chart():
    getData('COPPER', 'quarterly')
    trader.set_color_theme('turquoiseHexagon')
    trader.set_line_color("#0EE92B")
    trader.set_price_chart_type('Kagi')
    kagi = trader.get_kagi_instance()
    kagi.set_thick_line_color("#11e787")
    kagi.set_thin_line_color("#31553b")
    trader.open()


def coffee_chart():
    getData('COFFEE', 'annual')
    trader.set_color_theme('light')
    trader.set_positive_body_color("#1d5a1c")
    trader.set_negative_body_color("#6a1717")
    trader.set_price_chart_type('Renko')
    trader.open()


coffee_chart()


