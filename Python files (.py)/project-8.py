import lightningchart as lc
import pandas as pd
import os
from datetime import datetime
license_key_path = "LC-Python_License_key.txt" 
# Load the license key and initializing Python trader
license_key = open(license_key_path).read()
# File path to where the dataset is located, os.listdir lists all the files from the directory.
filepath = 'data/project-8/'
rates_csv = os.listdir(filepath)
fraud_dataframe = pd.read_csv(filepath + rates_csv[0])
lc.set_license(license_key)

# Convert the start date of the datatset to a unix time format in ms 
date_time = datetime.strptime('2013-09-01 00:00:00', "%Y-%m-%d %H:%M:%S")
unix_ms = date_time.timestamp() * 1000

# Only featues that can be identifies aka no PCA transformation
named_features_DF = fraud_dataframe[['Time', 'Amount', 'Class']]
# Only columns that have been transformed via principal component analysis
PCA_features_DF = fraud_dataframe.iloc[:, 1:29]
# Dataframes with only fraudulent transactions 
PCA_features_fraud_true = fraud_dataframe[fraud_dataframe.Class == 1].iloc[:, 1:29]

            
def chart1():
    """Plot with a line chart and a scatter chart"""

    new_chart = lc.ChartXY()

    # Line series
    x_plot = named_features_DF['Time'] * 1000
    y_plot_line = (named_features_DF['Amount'])
    
    # Dispose the default X axis and add a new one set to a date-time format
    default_x = new_chart.get_default_x_axis()
    default_x.dispose()
    new_X_axis = new_chart.add_x_axis()
    new_X_axis.set_tick_strategy('DateTime', time_origin=unix_ms)

    new_X_axis.set_title('Time elapsed in seconds')
    new_chart.default_y_axis.set_title('Transaction value')

    # Create a new lineseries
    new_series = new_chart.add_line_series(x_axis=new_X_axis)
    new_series.set_name('Transaction amount')
    new_series.add(x_plot, y_plot_line)

    # Add a scatter plot to the chart

    y_plot_scatter = named_features_DF['Class']
    # Add new Y axis to the chart for better viewing of the scatter pot
    scatter_Y_axis = new_chart.add_y_axis()
    # create a new scatter type series
    scatter_plot = new_chart.add_point_series(x_axis = new_X_axis, y_axis = scatter_Y_axis)
    scatter_plot.set_name('Fraud or not')
    scatter_plot.add(x_plot, y_plot_scatter)
    scatter_plot.set_palette_point_coloring(
            steps=[
            {'value': 1, 'color': '#FF0000'},
            {'value': 0, 'color': "#07CDF4"},         
        ],
        look_up_property='y',
        interpolate=True,
    )

    new_chart.open()


def chart2():
        """Generate a scatter plot for the PCA variables"""

        new_chart = lc.ChartXY()
        x_plot = fraud_dataframe['Time'] * 1000

        # Dispose the default X axis and add a new one set to a date-time format
        default_x = new_chart.get_default_x_axis()
        default_x.dispose()
        new_X_axis = new_chart.add_x_axis()
        new_X_axis.set_tick_strategy('DateTime', time_origin=unix_ms)
        new_chart.set_cursor_mode('show-nearest')

        # Colors used in the different scatter plots
        red = 0
        green = 255
        blue = 50
        # Loop through all PCA columns and create a scatter plot for each one
        for column in PCA_features_DF:
            y_plot = PCA_features_DF[column]
            # Modify the red and green values so plots become more red over time
            red += 8
            green -= 6
            scatter_series = new_chart.add_point_series()
            scatter_series.set_name(column)
            scatter_series.add(x_plot,y_plot)
            scatter_series.set_point_color((red, green, blue))
        new_chart.open()


def chart3(sort_type, data_source):
        """Create a polar heatmap. Set sort_type to either 0 for sectors or 1 for annuli.
        Set data source to 0 for full dataset or to 1 for only fradulent cases or 2 for sampled dataset"""
        
        new_chart = lc.PolarChart()
        heatmap_matrix = [] 

        for column in data_source:
            heatmap_list = []
            heatmap_list.append(data_source[column].values.tolist())
            heatmap_matrix.append(heatmap_list[0])

        annuli_count = len(heatmap_matrix[0])      
        sector_count = len(heatmap_matrix) 
        
        new_heatmap = new_chart.add_heatmap_series(
             sector_count, 
             annuli_count, 
             data_order=sort_type
        ) 

        if sort_type == 'sectors':
            new_radial =  new_chart.get_radial_axis()
            tick_list = [str(col) for col in data_source.columns]
            # Set the amount of divisions to match the amount of charted columns
            new_radial.set_division(len(tick_list))
            new_radial.set_tick_labels(tick_list)

        new_heatmap.invalidate_intensity_values(heatmap_matrix, 0, 0)
        new_heatmap.set_intensity_interpolation(True)
        new_heatmap.set_name(f'Sorted by {sort_type}, dataset size {len(data_source)}')
        new_heatmap.set_palette_coloring(
            steps=[
                {'value': 12, 'color': "#3700FF"},
                {'value': 6, 'color': "#00F2FF"},
                {'value': 0, 'color': "#08690FFF"},
                {'value': -6, 'color': "#CE7900"},
                {'value': -12, 'color': "#FF0000"},
            ],
            look_up_property='value',  
            interpolate=True  
        )
        new_chart.open()

PCA_features_sampled = PCA_features_DF.sample(1000)

# Sort types and data sources for the polar chart
data_sources = [PCA_features_DF, PCA_features_fraud_true, PCA_features_sampled]
data_orders = ['sectors', 'annuli']
chart3(sort_type=data_orders[0], data_source=data_sources[1])
# chart2()