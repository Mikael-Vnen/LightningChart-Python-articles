from lightningchart_trader import TAChart
import pandas as pd
import os
license_key_path = "Python-Trader_License_key.txt" 
# license key for python trader and the stock API
license_key = open(license_key_path).read()
chart = TAChart(license_key)
path_to_csv = 'data/project-12/'
# All file names in the filepath
csv_list = os.listdir(path_to_csv)
print(csv_list)
# Transform the CSV into a dataframe, combine the file path, with the desired files name 
stock_dataframe = pd.read_csv(path_to_csv + csv_list[4])
# Set chart title; I'm using the file name as a placeholder, 
# type; CandleStick, Bar, Line, Mountain, Renko, HeikinAshi or Point&Figure 
# and data source used; in this case the stock dataframe
chart.set_chart_title(csv_list[4])
chart.set_price_chart_type('Mountain') 
chart.set_data(stock_dataframe)
# Optional appearence customization
chart.set_color_theme('darkGold')
chart.set_line_color("#FCD601")
chart.change_time_range(0)
#chart.set_series_background_color('#45673C', fillStyle=1, gradientColor="#673628", angle=-168, gradientSpeed=0.80)
chart.open()
