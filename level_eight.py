# Level 8: Creating Database Tables
# 1. Design and create a database table to store sales data, including columns for product ID,
# sales amount, date, and customer ID.
# 2. Create a separate table to store product information, including product ID, name, category,
# and price.
# 3. Design a table to store customer information, including customer ID, name, email, and
# address.
# 4. Define relationships between the tables using foreign key constraints.
# 5. Populate the database tables with sample data from the sales dataset.
import csv
import logging
from datetime import datetime

from Connector import Connector

connector = Connector()
class Level_eight:
    def storeData(self,tableName,csvFile):
            # Read data from CSV file and insert into database
            con = connector.dbConnection()
            mydb = con.cursor()
            with open('csvFiles/'+csvFile, 'r', newline='', encoding='utf-8') as csvfile:
                csvreader = csv.reader(csvfile)
                next(csvreader)  # Skip header row if exists
                mydb.execute("SET foreign_key_checks = 0")
                for row in csvreader:
                    if tableName == 'Sales':
                        self.addToSalesTable(row,mydb)
                    elif tableName == 'Products':
                        self.addToProductsTable(row,mydb)
                    elif tableName == 'Regions':
                        self.addToRegionsTable(row,mydb)

                    else:
                        self.addToCustomersTable(row, mydb)
            # Commit changes and close connection
            con.commit()
            con.close()
            print("Data inserted into the {} table.".format(tableName))
            logging.info("Data inserted into the {} table.".format(tableName))
    def addToSalesTable(self,row,mydb):
        # Convert date string to datetime object and format it as YYYY-MM-DD
        date_str = datetime.strptime(row[4], '%d-%m-%Y').strftime('%Y-%m-%d')
        row[4] = date_str  # Replace the date string with the formatted date
        product_id = int(row[1])  # Assuming product_id is in the second column
        mydb.execute("SELECT 1 FROM products WHERE product_id = %s", (product_id,))
        if mydb.fetchone():
            query = "INSERT INTO Sales (sales_id, product_id, customer_id, sales_amount, date, region_id) VALUES (%s, %s, %s, %s, %s, %s)"
            mydb.execute(query, row)
    def addToProductsTable(self,row,mydb):
        query = "INSERT INTO Products (product_id,product_name,category,price) VALUES (%s, %s, %s, %s)"
        mydb.execute(query, row)
    def addToRegionsTable(self,row,mydb):
        query = "INSERT INTO Regions (region_id,region_name) VALUES (%s, %s)"
        mydb.execute(query, row)
    def addToCustomersTable(self,row,mydb):
        query = "INSERT INTO Customers (customer_id,customer_name,email,address) VALUES (%s, %s, %s, %s)"
        mydb.execute(query, row)

a = Level_eight()
a.storeData("Customers","customers.csv")
a.storeData("Regions","regions.csv")
a.storeData("Products","products.csv")
a.storeData("Sales","sales.csv")


