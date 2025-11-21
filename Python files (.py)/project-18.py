from lightningchart_trader import TAChart
import pandas as pd
import os
license_key_path = "Python-Trader_License_key.txt" 
# license key for python trader and the stock API
license_key = open(license_key_path).read()
chart = TAChart(license_key)
path_to_csv = 'data/project-18/'
# All file names in the filepath
csv_list = os.listdir(path_to_csv)
# Transform the CSV into a dataframe, combine the file path, with the desired files name 
stock_dataframe = pd.read_csv(path_to_csv + csv_list[0])
print(stock_dataframe.columns)
# New dataframe for the adjusted close price.
stock_dataframe.rename(columns={
    'Close' : 'Old close',
    'Adj Close' : 'close'}, inplace=True)
# Set chart title; I'm using the file name as a placeholder, 
# type; CandleStick, Bar, Line, Mountain, Renko, HeikinAshi or Point&Figure 
# and data source used; in this case the stock dataframe
chart.set_chart_title(csv_list[0])
chart.set_price_chart_type('CandleStick') 
chart.set_data(stock_dataframe)
# Optional appearence customization although I recommend changing the time range
chart.set_color_theme('darkGold')
chart.set_line_color("#b2ff24")
chart.set_series_background_color('#258382', fillStyle=1, gradientColor="#1a2765", angle=-173, gradientSpeed=0.80)
chart.add_relative_strength_index()
chart.add_bollinger_band()
chart.open()