import lightningchart as lc
from lightningchart import Themes
import pandas as pd
import os

license_key_path = "LC-Python_License_key.txt" 
# Load the license key and initializing Python trader
license_key = open(license_key_path).read()
# File path to where the dataset is located, os.listdir lists all the files from the directory.
filepath = 'data/project-10/'
rates_csv = os.listdir(filepath)
lc.set_license(license_key)
exchange_dataframe = pd.read_csv(filepath + rates_csv[0])

def set_date_axis(chart_instance):
        """Disposses the default x axis and creates a new one that uses the date-time format"""

        x_axis = chart_instance.add_x_axis()
        x_axis.set_tick_strategy('DateTime')
        chart_instance.get_default_x_axis().dispose()


def chart1():
    """Creates a new line chart"""
    
    new_chart = lc.ChartXY()
    set_date_axis(chart_instance=new_chart)
    USD_rate = exchange_dataframe[exchange_dataframe.currency == 'USD']
    name = USD_rate['currency_name'].head(1).to_string(index=False)
    # Set data sourcees for the axis
    x_plot = USD_rate['date'].to_list()
    y_plot = USD_rate['exchange_rate'].to_list()
    # Add a line plot to the chart instance
    new_series = new_chart.add_line_series()
    new_series.add(x_plot,y_plot)
    new_series.set_name(f'{name} exchange rate ')
    new_chart.open()


def chart2():
    "Chart two with multiple currency pairs"

    new_chart = lc.ChartXY()
    set_date_axis(chart_instance=new_chart)

    USD_rate = exchange_dataframe[exchange_dataframe.currency == 'USD']
    CNY_rate = exchange_dataframe[exchange_dataframe.currency == 'CNY']
    GBP_rate = exchange_dataframe[exchange_dataframe.currency == 'GBP']
    rates = [USD_rate, CNY_rate, GBP_rate]

    for cur in rates:
        # Set data sourcees for the axis
        x_plot = cur['date'].to_list()
        y_plot = cur['exchange_rate'].to_list()
        # Add a line plot to the chart instance
        new_series = new_chart.add_line_series()
        new_series.add(x_plot,y_plot)
        name = cur['currency_name'].head(1).to_string(index=False)
        new_series.set_name(f'{name} exchange rate ')
    new_chart.open()


def chart3():

    new_chart = lc.ChartXY()
    set_date_axis(chart_instance=new_chart)

    conversion_list = []
    USD_rate = exchange_dataframe[exchange_dataframe.currency == 'USD']
    GBP_rate = exchange_dataframe[exchange_dataframe.currency == 'GBP']

    for currency1, currency2 in zip(USD_rate['exchange_rate'], GBP_rate['exchange_rate']):
        conversion_list.append(currency1 - currency2)

    # Due to the exchange rate series being different in length they can't always be inserted right away
    # Insert mock data tot he beginning of the list
    while len(conversion_list) < len(GBP_rate['exchange_rate']):
        conversion_list.append(0)

    # Values used to calculate the scatter plot color map 
    currency1_max = max(USD_rate['exchange_rate'])
    currency2_max = max(GBP_rate['exchange_rate'])
    currency1_min = min(USD_rate['exchange_rate'])
    currency2_min = min(GBP_rate['exchange_rate'])

    # Drop the existing exchange rate column and replace it with the new one
    scatterDF = GBP_rate.drop(columns=['exchange_rate'],axis=1,inplace=False)
    scatterDF.insert(0, 'exchange_rate', conversion_list)

    x_plot = scatterDF['date'].to_list()
    y_plot = scatterDF['exchange_rate'].to_list()
    new_series = new_chart.add_point_series()
    new_series.add(x_plot,y_plot)
    new_series.set_name('exchange rate difference')
    new_series.set_palette_point_coloring(
            steps=[
            {'value': currency1_max - currency2_min, 'color': '#FF0000'},
            {'value': (currency1_max + currency2_max) / 2, 'color': "#D9F40C"},
            {'value': currency1_min - currency2_max, 'color': "#00FF0D"},
        ],
        look_up_property='y',
        interpolate=True,
    )

    rates = [USD_rate, GBP_rate]
    for cur in rates:
        # Set data sourcees for the axis
        x_plot = cur['date'].to_list()
        y_plot = cur['exchange_rate'].to_list()
        # Add a line plot to the chart instance
        new_series = new_chart.add_line_series()
        new_series.add(x_plot,y_plot)
    new_chart.open()

def chart4():

    new_chart = lc.BarChart(title='Median USD to EUR rate per year', theme=Themes.CyberSpace)
    USD_rate = exchange_dataframe[exchange_dataframe.currency == 'USD']
    bar_list = []

    # Yearly mean calculated for each bracket
    year_mean = 0
    # How many days or data points belong to that particular year
    date_count = 0
    # Current year
    df_year = 2025

    for date, rate in zip(USD_rate['date'], USD_rate['exchange_rate']):
        # Loop through the dataframe convert the date values to string 
        # and compare them to current year
        if str(df_year) in date:
            # As long as the year matches increment date count and add rate to the count
            year_mean += rate 
            date_count += 1
        else:
            # If the year doesn't match eg it has changed, calculate the mean from the current values
            # Decrement the year value by one and add the mean to a list
            year_mean = year_mean / date_count
            df_year -= 1
            bar_list.append({'category': f'Year {df_year}', 'value': year_mean})
            # Then reset the values 
            year_mean = rate
            date_count = 1
        
    # Set the bar chart properties and dataset
    new_chart.set_data(bar_list)
    new_chart.set_sorting('disabled')
    new_chart.open()
    
chart4()