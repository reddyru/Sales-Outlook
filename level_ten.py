# 1. Use historical sales data to create a time series array.
# 2. Visualize the original and smoothed time series using Matplotlib line plots.
# 3. Create word frequency arrays to identify common themes in customer reviews.
# 4. Visualize the word frequency distribution using Matplotlib histograms or word clouds.
# 5. Visualize statistical results using Matplotlib box plots, violin plots, or histograms.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

sales_data = pd.read_csv("csvFiles/sales.csv")

def createTimeSeries():
    # Convert 'date' column to datetime format
    sales_data['date'] = pd.to_datetime(sales_data['date'], format='%d-%m-%Y')
    # Group by date and sum the sales amounts
    time_series_data = sales_data.groupby('date')['sales_amount'].sum().reset_index()
    # Set 'date' column as index
    time_series_data.set_index('date', inplace=True)
    return time_series_data
def visualize(time_series_data):
    smoothed_time_series = time_series_data.rolling(window=7).mean()

    plt.figure(figsize=(10, 6))
    plt.plot(time_series_data.index, time_series_data['sales_amount'], label='Original')
    plt.plot(time_series_data.index, smoothed_time_series['sales_amount'], label='Smoothed', color='red')
    plt.title('Original vs Smoothed Time Series')
    plt.xlabel('Date')
    plt.ylabel('Sales Amount')
    plt.legend()
    plt.grid(True)
    plt.show()
time_series_data = createTimeSeries()
print(time_series_data)
visualize(time_series_data)
