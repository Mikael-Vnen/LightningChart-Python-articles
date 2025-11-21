from lightningchart_trader import TAChart
import pandas as pd
import os
license_key_path = "Python-Trader_License_key.txt" 
# license key for python trader and the stock API
license_key = open(license_key_path).read()
chart = TAChart(license_key)
path_to_csv = 'data/project-14/'
# All file names in the filepath
csv_list = os.listdir(path_to_csv)
print(csv_list)
# Create a new dashboard with two rows and a single column
new_dashboard = chart.create_dashboard(rows=2, cols=1)
# These values will be used to add charts to the dashboard
row_index = 0
for stock in csv_list:
    # Transform the CSV into a dataframe, combine the file path, with the desired files name 
    stock_dataframe = pd.read_csv(path_to_csv + stock)
    # A placeholder chart title, file name without the .csv
    chart_title = stock.removesuffix('.csv')
    stock_dataframe.rename(columns={
          'Open Price': 'open',
          'High Price': 'high',
          'Low Price': 'low',
          'Close Price': 'close'}, inplace=True)
    # Add a chart to the dashboard, then increment the row_index        
    dash_chart = new_dashboard.add_chart(chart_type='PointAndFigure', row_index=row_index, column_index=0, title=chart_title).set_data(stock_dataframe)
    row_index += 1
    # Optional appearence customization
    dash_chart.set_color_theme('darkGold')
    dash_chart.set_line_color("#65FC01")
    dash_chart.change_time_range(4)
chart.open()