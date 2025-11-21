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

# Parameters used in Alphavantages API, consult their documentation for more details. Only 'ticker' needs to be adjusted for this projects scope.
ticker_list = ['JNJ', 'PFE', 'MRK'] 

api_name = 'TIME_SERIES_DAILY_ADJUSTED'
outputsize = 'full'
ticker = ticker_list[2]
# API URL change the ticker_list[x] index to whichever company you want tot chart
template_url = f'https://www.alphavantage.co/query?function={api_name}&apikey={api_key}&outputsize={outputsize}&symbol={ticker}'

def api_call(template_url):
    """Make an API call for every URL passed to the function and convert the JSON respond to a Python dictionary"""
    
    request = requests.get(template_url).json()
    data_key = list(request.keys())
    # Formatting the API data for the Trader chart.
    data_list = []
    for date, value in request[data_key[1]].items():
        # Data needs to be in this order for the trader to work. Open,High,Low,Close,Volume(optional),Date.
        # Dictionaries returned by the API use date as the dictionary key
        data_list.append({'open': float(value['1. open']), 
                          'high': float(value['2. high']), 
                          'low': float(value['3. low']), 
                          'close': float(value['4. close']), 
                          'volume': float(value['6. volume']), 
                          'date': date})

    # Adding the data to the chart and setting chart title to the ticker
    title_key = request[data_key[0]]['2. Symbol']
    trader.set_data(data_list)
    trader.set_chart_title(title_key)
    

api_call(template_url)
# Set chart customization and indicators 
trader.add_simple_moving_average(period_count=5)
trader.add_moving_average_convergence_divergence()
trader.add_volume()
trader.add_relative_strength_index(period_count=5)
trader.change_time_range(2)
trader.open()
    


