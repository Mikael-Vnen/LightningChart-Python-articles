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
api_key = open(api_key_path).read()

# Variables used for the API call. 
# More information regarding these can be found from Alphavantages documentation
api_name = 'TIME_SERIES_DAILY_ADJUSTED'
ticker = 'AAPL'
outputsize = 'full'


def stock_api_call(template):
    """Getting the stock data from the API.  Time out in 5 seconds in case the API doesn't respond (optional)"""

    print(template)
    r = requests.get(template, timeout=5).json()
    # Get the second dictionarys key
    series_key = list(r.keys())[1]   
    # Formatting the API data for the Trader chart
    data_list = []
    for y, x in r[series_key].items():
        # Converted the data from string to float
        # Add the dictionary z to a list that is then imported to the trader
        data_list.append({'open':float(x['1. open']),
                          'high':float(x['2. high']),
                          'low':float(x['3. low']),
                          'close':float(x['4. close']),
                          'volume':float(x['6. volume']),
                          'date':y})  
    # Adding the data to the chart
    trader.set_data(data_list)


def apply_default_style():

    #Change background
    trader.set_color_theme('cyberSpace')
    #Set colours for the candlesticks
    trader.set_positive_body_color('#0fdf0c')
    trader.set_positive_wick_color("#68d991")
    trader.set_negative_body_color("#f31616")
    trader.set_negative_wick_color("#d75b5b")
    #set the chart type.
    trader.set_price_chart_type('CandleStick')

    
def open_chart1():
    
    template_url = f'https://www.alphavantage.co/query?function={api_name}&symbol={ticker}&apikey={api_key}&outputsize={outputsize}'
    #Calls the api function with the specified url.
    stock_api_call(template_url)
    apply_default_style()
    #Add technical indicators
    trader.add_bollinger_band(period_count=14)
    trader.set_chart_title(f'{ticker} stock data')
    #Open the chart
    trader.open()


def open_chart2():
    
    template_url = f'https://www.alphavantage.co/query?function={api_name}&symbol={ticker}&apikey={api_key}&outputsize={outputsize}'
    # Make an API with the specified url.
    stock_api_call(template_url)
    apply_default_style()
    trader.set_chart_title(f'{ticker} stock data')
    trader.add_relative_strength_index()
    trader.add_moving_average_convergence_divergence()
    #Open the chart
    trader.open()


def open_chart3():
   
    template_url = f'https://www.alphavantage.co/query?function={api_name}&symbol={ticker}&apikey={api_key}&outputsize={outputsize}'
    # Make an API with the specified url.
    stock_api_call(template_url)
    apply_default_style()
    #Add technical indicators
    trader.add_on_balance_volume()
    trader.set_chart_title(f'{ticker} stock data')
    #Open the chart
    trader.open()
    

open_chart1() 
    
    
    
    




         
         
   
    



    


   
    


