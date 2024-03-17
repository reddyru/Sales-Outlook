# Level 1: Data Loading and Basic Analysis
# 1. Load the sales dataset (e.g., 'sales.csv') into a Pandas DataFrame.
# 2. Display the first 5 rows of the dataset.
# 3. Check the shape (number of rows and columns) of the dataset.
# 4. Display basic statistics (mean, median, min, max) for the 'Sales' column.
# 5. Determine the number of unique products sold.


import numpy as np
import matplotlib as mat
import pandas as pd

salesData = pd.read_csv("csvFiles/sales.csv")

print(salesData.head(6))
print("Shape of dataset: ",salesData.shape)
print("Mean of Sales amount: ",salesData['sales_amount'].mean())
print("Median of Sales amount: ",salesData['sales_amount'].median())
print("Min of Sales amount: ",salesData['sales_amount'].min())
print("Max of Sales amount: ",salesData['sales_amount'].max())
print("The number of unique products sold:",salesData['product_id'].nunique())
