from lightningchart_trader import TAChart
import pandas as pd
import os
license_key_path = "Python-Trader_License_key.txt" 
# license key for python trader and the stock API
license_key = open(license_key_path).read()
chart = TAChart(license_key)
path_to_csv = 'data/project-11/'
# All file names in the filepath
csv_list = os.listdir(path_to_csv)
print(csv_list)
# Create a new dashboard with two rows and a two column
new_dashboard = chart.create_dashboard(rows=2, cols=2)
# These values will be used to add charts to the dashboard
row_index = 0
col_index = 0
# Loop though files other than the chemical index and add them to the dashboard
for index in range(4):
    # Transform the CSV into a dataframe, combine the file path, with the desired files name 
    stock_dataframe = pd.read_csv(path_to_csv + csv_list[index])
    chart_title = csv_list[index].removesuffix('.csv')
    # rename date column 
    stock_dataframe = stock_dataframe.rename(columns={'Unnamed: 0' : 'date'})
    # Add a chart to the dashboard witht he following parameters      
    dash_chart = new_dashboard.add_chart(chart_type='Line', 
                                         row_index=row_index, column_index=col_index,  
                                         title=chart_title).set_data(stock_dataframe)
    # Place charts to the dashboard based on the current column and row index
    col_index += 1
    if col_index >= 2:
        col_index = 0
        row_index += 1
    # Optional appearence customization
    dash_chart.set_line_color("#65FC01")
    dash_chart.change_time_range(2)   
    dash_chart.add_volume() 
chart.open()
