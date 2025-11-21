from lightningchart_trader import TAChart
import pandas as pd
import os
from datetime import datetime
license_key_path = "Python-Trader_License_key.txt" 
# license key for python trader and the stock API
license_key = open(license_key_path).read()
chart = TAChart(license_key)
path_to_csv = 'data/project-15/'
# All file names in the filepath
csv_list = os.listdir(path_to_csv)

def preprocess(bond_term, country, source_df):
    "Perfrom any needed preprocessing to the data"

    # Only include bond data from that specific country
    filtered_df = source_df.filter(like=country, axis='columns')

    # Insert the time column into the new dataframe, with the filtered country columns
    filtered_df.insert(0, 'time', source_df['time'])

    # Change the time format from unix timestamp (ms) in to a readable date format (yyyy-mm-dd)
    date_list = [datetime.fromtimestamp(date/1000).strftime('%Y-%m-%d') 
                 for date in filtered_df['time']]
    
    # Use the price column for all the OHLC value fields.
    value_list = filtered_df[bond_term].to_list()
    # Insert the ohlc values and date in to dictionary then append that dictionary into a list to be used as a data source
    return [{'open': val, 'high': val, 'low': val, 'close': val, 'date': date} 
            for val, date in zip(value_list, date_list)]


def chart1():
    # Create dashboard, with x row(s) and x column(s)
    new_dashboard = chart.create_dashboard(2, 1)
    # Indexes used to postiion charts to the dashboard
    row_index = 0
    column_index = 0
    # Country and their respective bonds used for dashboard
    countries = ['US']
    bond_term = ['US10']
    price_df = pd.read_csv(path_to_csv + csv_list[0])
    yields_df = pd.read_csv(path_to_csv + csv_list[1])
    bond_index = 0
    for country in countries:
        # Create a chart for bond prices and increment column index
        chart_list = preprocess(bond_term=bond_term[bond_index], country=country, source_df=price_df) 
        dashboard_chart = new_dashboard.add_chart('Line', row_index, column_index).set_data(chart_list) 
        dashboard_chart.set_chart_title(f"Bond prices for {bond_term[bond_index]}")
        row_index += 1
        # Another one for bond yields
        chart_list = preprocess(bond_term=bond_term[bond_index], country=country, source_df=yields_df) 
        dashboard_chart = new_dashboard.add_chart('Line', row_index, column_index).set_data(chart_list) 
        dashboard_chart.set_chart_title(f"Bond yields for {bond_term[bond_index]}")
        dashboard_chart.set_color_theme('darkGold')
    chart.open()


def chart2():
    # Create dashboard, with x row(s) and x column(s)
    new_dashboard = chart.create_dashboard(2, 2)
    # Indexes used to postiion charts to the dashboard
    row_index = 0
    column_index = 0
    # Country and their respective bonds used for dashboard
    countries = ['US', 'GB']
    bond_term = ['US10', 'GB10']
    price_df = pd.read_csv(path_to_csv + csv_list[0])
    yields_df = pd.read_csv(path_to_csv + csv_list[1])
    bond_index = 0
    for country in countries:
        # Create a chart for bond prices and increment column index
        chart_list = preprocess(bond_term=bond_term[bond_index], country=country, source_df=price_df) 
        dashboard_chart = new_dashboard.add_chart('Line', row_index, column_index).set_data(chart_list) 
        dashboard_chart.set_chart_title(f"Bond prices for {bond_term[bond_index]}")
        column_index += 1
        # Another one for bond yields
        chart_list = preprocess(bond_term=bond_term[bond_index], country=country, source_df=yields_df) 
        dashboard_chart = new_dashboard.add_chart('Line', row_index, column_index).set_data(chart_list) 
        dashboard_chart.set_chart_title(f"Bond yields for {bond_term[bond_index]}")
        # Reset column index and increment row and bond indexes
        column_index = 0
        row_index += 1
        bond_index += 1
        dashboard_chart.set_color_theme('darkGold')
    chart.open()


def chart3():
    # Create dashboard, with x row(s) and x column(s)
    new_dashboard = chart.create_dashboard(2, 2)
    row_index = 0
    column_index = 0
    # Country used for dashboard
    country = 'US'
    # Bond terms from the selected country
    bond_term = ['US01', 'US05', 'US10', 'US20',]
    # Source either prices.csv [0] or yields.csv [1]
    source_df = pd.read_csv(path_to_csv + csv_list[1])
    for bond_term in bond_term: 
        chart_list = preprocess(bond_term, country, source_df) 
        dashboard_chart = new_dashboard.add_chart('Line', row_index, column_index).set_data(chart_list) 
        dashboard_chart.set_chart_title(f"{country} bond yields for {bond_term}") 
        # Position the charts to the dashboard
        column_index += 1
        if column_index >= 2:
            column_index = 0
            row_index += 1
        
        dashboard_chart.set_color_theme('darkGold')
    chart.open()


def chart4():
    # Create dashboard, with x row(s) and x column(s)
    new_dashboard = chart.create_dashboard(2, 2)
    row_index = 0
    column_index = 0
    # Country used for dashboard
    country = 'US'
    # Bond terms from the selected country
    bond_term = ['US01', 'US05', 'US10', 'US20',]
    # Source either prices.csv [0] or yields.csv [1]
    source_df = pd.read_csv(path_to_csv + csv_list[1])
    for bond_term in bond_term: 
        chart_list = preprocess(bond_term, country, source_df) 
        dashboard_chart = new_dashboard.add_chart('Renko', row_index, column_index).set_data(chart_list) 
        dashboard_chart.set_chart_title(f"{country} bond yields for {bond_term}") 
        # Position the charts to the dashboard
        column_index += 1
        if column_index >= 2:
            column_index = 0
            row_index += 1
        
        dashboard_chart.set_color_theme('darkGold')
    chart.open()
chart1()