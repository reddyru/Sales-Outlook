import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def infer_customer_segment(email):
    if "@example.com" in email:
        return "Example Customers"
    else:
        return "Other Customers"

#level 1: data Loading and Basic Analysis

sdf = pd.read_csv('sales.csv')# 1.1 Now 'df' is your DataFrame containing the data from the CSV file
pdf=pd.read_csv('products.csv') # loading products file
rdf=pd.read_csv('regions.csv') # loading regions file
cdf = pd.read_csv('customers.csv')#loading customers file

print(sdf.head(5)) # 1.2 display first 5 rows of sales

print("Shape of the database:", sdf.shape) # 1.3 shape of the dataset

sales_column = sdf['sales_amount']  # 1.4 Selecting the 'Sales' column
print("Mean:", sales_column.mean())
print("Median:", sales_column.median())
print("Minimum:", sales_column.min())
print("Maximum:", sales_column.max())

num_unique_products = pdf['product_name'].nunique()# 1.5 num of unique prod sold
print("Number of unique products:", num_unique_products)


# Level 2: Data Cleaning and Preprocessing

missing_values = sdf.isnull().sum() # 2.1 Check for missing values using isnull()

print("Number of missing values in each sales data:")
print(missing_values)

missing_values = pdf.isnull().sum()

print("Number of missing values in each prod data:")
print(missing_values)

missing_values = rdf.isnull().sum()

print("Number of missing values in each region data:")
print(missing_values)

missing_values = cdf.isnull().sum()

print("Number of missing values in each customers data:")
print(missing_values)


rdf['region_id_encoded'], _ = pd.factorize(rdf['region_name'])# 2.2 Perform label encoding on region
# Display the encoded DataFrame
print(rdf) 

# label encoding on product
pdf['category_encoded'], _ = pd.factorize(pdf['category'])
# Display the encoded DataFrame
print(pdf)



duplicate_rows = sdf[sdf.duplicated()] # 2.3 duplicate rows in sales
print("Duplicate rows in sales:")
print(duplicate_rows)

# duplicate rows in products
duplicate_rows = pdf[pdf.duplicated()]
print("Duplicate rows in products:")
print(duplicate_rows)

# dupliate rows in regions
duplicate_rows = rdf[rdf.duplicated()]
print("Duplicate rows in regions:")
print(duplicate_rows)

# dupliate rows in customers
duplicate_rows = cdf[cdf.duplicated()]
print("Duplicate rows in customers:")
print(duplicate_rows)


min_sales_amount = sdf['sales_amount'].min() # 2.4 Normalize the 'Sales' column to a scale between 0 and 1.
max_sales_amount = sdf['sales_amount'].max()

# Perform Min-Max scaling to normalize the 'sales_amount' column
sdf['sales_amount_normalized'] = (sdf['sales_amount'] - min_sales_amount) / (max_sales_amount - min_sales_amount)

# Display the DataFrame with normalized 'sales_amount' column
print(sdf)


q1 = sdf['sales_amount'].quantile(0.25)  # 2.5 Identify and remove outliers from the database using appropriate techniques.
q3 = sdf['sales_amount'].quantile(0.75)
iqr = q3 - q1
outliers_iqr = sdf[(sdf['sales_amount'] < q1 - 1.5 * iqr) | (sdf['sales_amount'] > q3 + 1.5 * iqr)]
print("identified outliers \n" , outliers_iqr)

# Remove outliers identified by the IQR method
sdf = sdf.drop(outliers_iqr.index)
print("after removal of outliers \n" , sdf)


# Level 3: Exploratory Data Analysis (EDA)

# 3.1. Visualize the distribution on sales amounts using a histogram.

plt.figure(figsize=(10, 6)) # 3.1 Plot the histogram of sales amounts
plt.hist(sdf['sales_amount'], bins=20, color='skyblue', edgecolor='black')
plt.title('Distribution of Sales Amounts')
plt.xlabel('Sales Amount')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()


plt.figure(figsize=(8, 6)) # 3.2 boxplot for outliers in sales 
plt.boxplot(sdf['sales_amount'])
plt.title('Boxplot of Sales Amounts')
plt.ylabel('Sales Amount')
plt.grid(True)
plt.show()

# 3.3 relationship between sales and other variables using scatter plot

# Scatter plot for Product ID vs. Sales
plt.scatter(sdf['product_id'], sdf['sales_amount'])
plt.xlabel('Product ID')
plt.ylabel('Sales Amount')
plt.title('Product ID vs. Sales')
plt.show()

# Scatter plot for Customer ID vs. Sales
plt.scatter(sdf['customer_id'], sdf['sales_amount'])
plt.xlabel('Customer ID')
plt.ylabel('Sales Amount')
plt.title('Customer ID vs. Sales')
plt.show()

# Scatter plot for Region ID vs. Sales
plt.scatter(sdf['region_id'], sdf['sales_amount'])
plt.xlabel('Region ID')
plt.ylabel('Sales Amount')
plt.title('Region ID vs. Sales')
plt.show()


corr_matrix = sdf.corr() # 3.4 Calculate the correlation matrix

# Visualize the correlation matrix
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title('Correlation Matrix')
plt.show()


sdf['date'] = pd.to_datetime(sdf['date'],format="%d-%m-%Y") # 3.5 Analyze the sales trend over time using line plots or time series plots. 
# Convert the 'date' column to datetime 

# Group the data by date and calculate the total sales for each day
daily_sales = sdf.groupby('date')['sales_amount'].sum()

# Plot the sales trend over time
plt.figure(figsize=(10, 6))
plt.plot(daily_sales.index, daily_sales.values, marker='o', linestyle='-')
plt.title('Sales Trend Over Time')
plt.xlabel('Date')
plt.ylabel('Total Sales Amount')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# Level 4: Data Aggregaton and Grouping

# 4.1 Group the sales data by product category and calculate the total sales amount for each category.
merge_pdf_sdf = pd.merge(sdf,pdf,on='product_id') 
category_sales=merge_pdf_sdf.groupby('category')['sales_amount'].sum().reset_index()

print(category_sales)

# 4.2 Group the sales data by month and year and calculate the average sales amount for each month

sdf['date']=pd.to_datetime(sdf['date'],format="%m-%y")
sdf['month_year']=sdf['date'].dt.to_period('m')
avg_sales=sdf.groupby('month_year')['sales_amount'].mean().reset_index()
print("Avg sales: ", avg_sales)

# 4.3 Aggregate the sales data by region and calculate the total sales amount for each region.
merge_rdf_sdf=pd.merge(rdf,sdf,on='region_id')
total_sales_region = merge_rdf_sdf.groupby('region_id')['sales_amount'].sum().reset_index()
print("Total sales per region: ", total_sales_region)

# 4.4 Group the sales data by customer segment and calculate the average sales amount for each segment.

merge_pdf_cdf = pd.merge(sdf,cdf,on='customer_id') 
merge_pdf_cdf["customer_segment"] = merge_pdf_cdf["email"].apply(infer_customer_segment)
average_sales_by_segment = merge_pdf_cdf.groupby("customer_segment")["sales_amount"].mean().reset_index()

print("category segment avg" , average_sales_by_segment)

# 4.5. Aggregate the sales data by sales representative and calculate the total sales amount for each representative.



# Level 5: Data Visualizaton with Matplotlib

# 1. Create a bar chart to visualize the total sales amount by product category.

category_sales=merge_pdf_sdf.groupby('category')['sales_amount'].sum()

# Plotting
plt.figure(figsize=(10, 6))
category_sales.plot(kind='bar', color='skyblue') 
# from 4.1
plt.title('Total Sales Amount by Product Category')
plt.xlabel('Product Category')
plt.ylabel('Total Sales Amount')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()



# 5.2 and 3.5 are same Plotting line plot to show sales trend over time 


# 5.3 Create a pie chart to represent the distribuAon of sales across different regions.

# Plotting
total_sales_region = merge_rdf_sdf.groupby('region_id')['sales_amount'].sum()
plt.figure(figsize=(8, 8))
plt.pie(total_sales_region, labels=total_sales_region.index, autopct='%1.1f%%', startangle=140)
plt.title('Distribution of Sales Across Regions')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
plt.show()

# 5.4 Generate a boxplot to compare the sales performance of diferent customer segments.

# Generate the boxplot
category_sales_avg=merge_pdf_sdf.groupby('category')['sales_amount'].mean()
plt.figure(figsize=(10, 6))
plt.boxplot(category_sales_avg)
plt.xlabel('Sales Amount')
plt.ylabel('Customer Segment')
plt.title('Sales Performance by Customer Segment')
plt.grid(False)
plt.show()    

# 5.5 Visulaize the relationship between sales and advertising expenditure using a scatter plot

# Level 6: Advanced Data Manipulaton with Numpy

# 6.1. Use Numpy to calculate the mean, median, and standard deviation of the sales data.

mean = np.mean(sdf['sales_amount'])
median = np.median(sdf['sales_amount'])
std=np.std(sdf['sales_amount'])
print("mean: ",mean)
print("median: " , median)
print("standard deviation : ", std)

# 6.2 perform element wise arithmetic operation on the sales data ( add, sub, multiplication)

# Define a scalar value for demonstration
scalar_value = 10

# Perform element-wise addition
sales_data_addition = sdf['sales_amount'] + scalar_value

# Perform element-wise subtraction
sales_data_subtraction = sdf['sales_amount']  - scalar_value

# Perform element-wise multiplication
sales_data_multiplication = sdf['sales_amount'] * scalar_value

# Display the results
print("Sales data after addition:", sales_data_addition)
print("Sales data after subtraction:", sales_data_subtraction)
print("Sales data after multiplication:", sales_data_multiplication)


# 6.3 use numpy to reshape the sales data into a different dimension
print("Original shape of the sales database:", sdf.shape)
print(sdf.head())
new_sdf=np.reshape(np.array(sdf),(98,-1))
print(new_sdf.shape)

# 6.4 apply brodcasting to perform operations on arrays with different shapes 

# Extract the 'sales_amount' column as a NumPy array
sales_amount = sdf['sales_amount'].values

# Generate an array with different shape (e.g., a single value)
broadcast_array = np.array([100])

#Add broadcast_array to sales_amount
result_addition = sales_amount + broadcast_array

# Subtract 
result_subtraction = sales_amount - broadcast_array

#  Multiply
result_multiplication = sales_amount * broadcast_array

#  Divide 
result_division = sales_amount / broadcast_array


print("Result of broadcasting addition:")
print(result_addition)
print("\nResult of broadcasting subtraction:")
print(result_subtraction)
print("\nResult of broadcasting multiplication:")
print(result_multiplication)
print("\nResult of broadcasting division:")
print(result_division)

# 6.5 use numpy to perform matrix multiplication on sales data arrays


# Convert relevant columns to NumPy arrays
product_id = sdf['product_id'].values
customer_id = sdf['customer_id'].values
sales_amount = sdf['sales_amount'].values

# Perform matrix multiplication
# Note: We'll multiply product_id with customer_id
result_matrix_multiplication1 = np.matmul(product_id.reshape(-1, 1), customer_id.reshape(1, -1))
result_matrix_multiplication2 = np.matmul(product_id.reshape(-1, 1), sales_amount.reshape(1, -1))

# Print the result
print("Result of matrix multiplication between product_id and customer_id:")
print(result_matrix_multiplication1)

print("Result of matrix multiplication between product_id and sales_amount:")
print(result_matrix_multiplication2)

# Convert 'date' column to datetime type
sdf['date'] = pd.to_datetime(sdf['date'])

# Filter sales data for a specific time period (e.g., year 2023)
sdf_2023 = sdf[sdf['date'].dt.year == 2023]
print("after filtering\n",sdf_2023)

# Assuming you have loaded products df from "products.csv"
electronics_products = pdf[pdf['category'] == 'Electronics']
electronics_product_ids = electronics_products['product_id'].tolist()

# Select rows where sales amount is greater than 1000 and the product category is 'Electronics'
electronics_sales = sdf[(sdf['sales_amount'] > 1000) & (sdf['product_id'].isin(electronics_products['product_id']))]
print("7.2 : \n",electronics_sales)


# Calculate total sales amount and average sales amount per product category
sales_with_products = pd.merge(sdf, pdf, on='product_id', how='inner')
sales_by_category = sales_with_products.groupby('category').agg(total_sales=('sales_amount', 'sum'),average_sales=('sales_amount', 'mean'))
print("7.3 : \n",sales_by_category)


# Merge sales data with customer data based on customer ID
merged_df = pd.merge(sdf, cdf, on='customer_id', how='inner')

# Join sales data with product data based on product ID using .join() method
sales_product_df = sdf.set_index('product_id').join(pdf.set_index('product_id'))
print("7.4 :\n",sales_product_df)















