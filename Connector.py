import csv
from datetime import datetime

import mysql.connector 
import mailbox
import logging

class Connector:
    def dbConnection(self):
        try:
            # Establish a connection to the MySQL database
            con = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="admin123",
                database="AITraining"
            )
            print("Connected to the database.")
            logging.basicConfig(filename="project.log", encoding="utf-8", level=logging.DEBUG)
            logging.info("Connected to database.")
        except mysql.connector.Error as e:
            print("Error connecting to MySQL database:", e)
            logging.error("Error connecting to MySQL database:", exc_info=True)
        return con
    def retreiveFromDB(self, option):
        con = self.dbConnection()
        mydb = con.cursor()
        if option == "byCategory":
            query = """
            SELECT category, SUM(sales_amount) AS total_sales_amount
            FROM Sales
            JOIN Products ON Sales.product_id = Products.product_id
            GROUP BY category;"""
        elif option == "byProduct":
            query = """
                SELECT s.sales_id,s.product_id,p.product_name,p.category,p.price,
                    s.customer_id,s.sales_amount,s.date,s.region_id FROM Sales s JOIN
                    Products p ON s.product_id = p.product_id;"""
        elif option == "highestPurchase":
            highestPurchase = """SELECT MAX(sales_amount) FROM Sales;"""
            mydb.execute(highestPurchase)
            highestPurchase = mydb.fetchone()[0]
            query = f"""SELECT customer_id FROM Sales WHERE sales_amount = {highestPurchase};"""
        elif option == "by_month_and_year":
            query = """
                SELECT YEAR(date) AS year, MONTH(date) AS month, AVG(sales_amount) AS average_sales_amount
                FROM Sales
                GROUP BY YEAR(date), MONTH(date);
            """
        else:
            query = """
                SELECT r.region_name, p.product_id, p.product_name, SUM(s.sales_amount) AS total_sales_amount
                FROM Sales s
                JOIN Products p ON s.product_id = p.product_id
                JOIN Regions r ON s.region_id = r.region_id
                GROUP BY r.region_name, p.product_id, p.product_name
                ORDER BY r.region_name, total_sales_amount DESC;
            """

        mydb.execute(query)
        rows = mydb.fetchall()
        mydb.close()
        con.close()
        return rows


