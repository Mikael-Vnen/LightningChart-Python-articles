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
# List for adding data to the chart
data = []

def getData(ticker, api_name):
    "Get data from Alphavantages API and modify it to form that can be used by Python Trader"

    # Getting the stock data from the API
    url = f'https://www.alphavantage.co/query?function={api_name}&symbol={ticker}&apikey={key}'
    api_request = requests.get(url)
    api_dict = api_request.json()
    # The API returns two dictionaries, one for metadata and one for the stock data itself
    keys = list(api_dict.keys())
    # Get the second dictionary key (stock data) and store it in a variable
    keys = keys[1]
    # Formatting the API data for the Trader 
    for date, ohlc_dict in api_dict[keys].items():
        # Convert OHLC values to float and and add them to the data list as a dictionary
        data.append({'open': float(ohlc_dict['1. open']),
                     'high': float(ohlc_dict['2. high']),
                     'low': float(ohlc_dict['3. low']),
                     'close': float(ohlc_dict['4. close']),
                     'date':date})
    # Use the list of dictionaries as a data source for the chart      
    trader.set_data(data)
    # Get data regarding this particular ticker symbol using the ticker search API
    ticker_search = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={ticker}+&apikey={key}'
    ticker_info = requests.get(ticker_search)
    ticker_info = ticker_info.json()
    # Get the company name from the top search result fot he chart title
    ticker_name = ticker_info['bestMatches'][0]['2. name']
    trader.set_chart_title(ticker_name +' stock data')

      
def chart1():
    """Candle stick chart example"""

    getData(ticker='MSFT', api_name='TIME_SERIES_DAILY')
    # Optinal customization
    trader.set_color_theme('cyberSpace')
    trader.set_price_chart_type('CandleStick')
    
    trader.set_positive_body_color('#0fdf0c')
    trader.set_positive_wick_color('#33d7a0')
    trader.set_negative_body_color("#f3eb16")
    trader.set_negative_wick_color('#b85900')
    # Open the chart
    trader.open()


def chart2():
    """Bar chart example"""

    getData(ticker='NVDA', api_name='TIME_SERIES_DAILY')
    trader.set_color_theme('cyberSpace')
    trader.set_price_chart_type('Bar')

    trader.set_positive_body_color("#0C28B6")
    trader.set_positive_wick_color('#8724EB')
    trader.set_negative_body_color("#F316A2")
    trader.set_negative_wick_color('#882555')
    trader.open()


def chart3():
    """Mountain chart example"""

    getData(ticker='TSLA', api_name='TIME_SERIES_DAILY')
    trader.set_color_theme('darkGold')
    trader.set_price_chart_type('Mountain')
    trader.open()


def chart4():
    """Line chart example with added technical indicators"""

    getData('GME', api_name='TIME_SERIES_MONTHLY')
    trader.set_color_theme('turquoiseHexagon')
    # add the technical indicators standart deviation, HVI and HML
    trader.add_standard_deviation(period_count=20)
    trader.add_historical_volatility_index()
    trader.add_high_minus_low()
    trader.set_price_chart_type('Mountain')
    # Open the chart
    trader.open()


def chart5():
    """Example of a Heikin Ashi chart"""

    getData('TSLA', api_name='TIME_SERIES_MONTHLY')
    trader.set_color_theme('lightNature')
    trader.set_price_chart_type('HeikinAshi')
    trader.open()


def chart6():
    """Example of a renko chart"""

    getData('NOK', api_name='TIME_SERIES_MONTHLY')
    trader.set_color_theme('light')
    trader.set_positive_body_color("#1d5a1c")
    trader.set_negative_body_color("#6a1717")
    trader.set_price_chart_type('Renko')
    trader.open()


def chart7():
    """Example of a Kagi chart"""

    getData('BRK-A', api_name='TIME_SERIES_MONTHLY')
    trader.set_color_theme('cyberSpace')
    trader.set_price_chart_type('Kagi')
    kagi = trader.get_kagi_instance()
    kagi.set_thick_line_color("#11e787")
    kagi.set_thin_line_color("#31553b")
    trader.open()


def chart8():
    """Example of a point and figure chart"""

    getData('RTX', api_name='TIME_SERIES_MONTHLY')
    trader.set_color_theme('darkGold')
    trader.set_price_chart_type('PointAndFigure')
    trader.open()


chart8()

