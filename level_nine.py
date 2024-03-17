from Connector import Connector

connector = Connector()

class level_eight:
    def retrieve_total_sales_by_category(self):
        rows = connector.retreiveFromDB("byCategory")
        if rows:
            print("Total sales amount for each product category:")
            for row in rows:
                sale_data = {
                    "category": row[0],
                    "total_sales_amount": str(row[1])
                }
                print(sale_data)
        else:
            print("No data")
    def retrieve_sales_with_products(self):
        rows = connector.retreiveFromDB("byProduct")
        if rows:
            print("Total sales amount for each product category:")
            for row in rows:
                sale_data ={
                    "sales_id": row[0],
                    "product_id":row[1],
                    "product_name":row[2],
                    "category":row[3],
                    "price":row[4],
                    "customer_id":row[5],
                    "sales_amount":str(row[6]),
                    "date":row[7],
                    "region_id":row[8]

                }
                print(sale_data)
        else:
            print("No data")
    def retrieve_customers_with_highest_purchase(self):
        rows = connector.retreiveFromDB("highestPurchase")
        print("Customers with the highest purchase:")
        for row in rows:
            print(row[0])
    def calculate_average_sales_by_month_and_year(self):
        rows = connector.retreiveFromDB("by_month_and_year")
        print("Average sales amount by month and year:")
        for row in rows:
            print(f"Year: {row[0]}, Month: {row[1]}, Average Sales Amount: {row[2]}")
    def find_top_selling_products_by_region(self):
        rows = connector.retreiveFromDB("topSellingbyRegion")
        print("Top-selling products by region:")
        for row in rows:
            sale_data = {
                "region_name":row[0],
                "product_id":row[1],
                "product_name":row[2],
                "total sale amount":str(row[3])
            }
            print(sale_data)


a = level_eight()
a.retrieve_total_sales_by_category()
a.retrieve_sales_with_products()
a.retrieve_customers_with_highest_purchase()
a.calculate_average_sales_by_month_and_year()
a.find_top_selling_products_by_region()