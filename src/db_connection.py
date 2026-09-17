import os
from dotenv import load_dotenv
import pandas as pd
import mysql.connector
from mysql.connector import Error

# Load environment variables
load_dotenv()

connection = None
cursor = None

try:
    # Connect to MySQL
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    print("MySQL connected successfully.")

    cursor = connection.cursor()

    # Verify database connection
    cursor.execute("SELECT DATABASE();")
    database_name = cursor.fetchone()

    print("Connected Database:", database_name[0])

    # Load cleaned transaction data
    df = pd.read_csv(
        "data/processed/cleaned_transactions.csv"
    )

    print("Rows ready for MySQL:", len(df))

    # Columns required for transactions
    columns_to_insert = [
        "order_id",
        "customer_id",
        "product_id",
        "order_date",
        "quantity",
        "unit_price",
        "unit_cost",
        "category",
        "region"
    ]

    # Prepare transaction records
    records = [
        tuple(
            value.item() if hasattr(value, "item") else value
            for value in row
        )
        for row in df[columns_to_insert].values
    ]

    print("Transactions prepared:", len(records))

    # Prepare unique customers
    customer_records = [
        (customer_id,)
        for customer_id in df["customer_id"].drop_duplicates()
    ]

    print("Customers prepared:", len(customer_records))

    # Prepare unique products
    product_records = [
        (product_id,)
        for product_id in df["product_id"].drop_duplicates()
    ]

    print("Products prepared:", len(product_records))

    # SQL queries
    customer_insert_query = """
    INSERT INTO customers (customer_id)
    VALUES (%s)
    """

    product_insert_query = """
    INSERT INTO products (product_id)
    VALUES (%s)
    """

    transaction_insert_query = """
    INSERT INTO transactions
    (
        order_id,
        customer_id,
        product_id,
        order_date,
        quantity,
        unit_price,
        unit_cost,
        category,
        region
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Clear old data
    # Child table must be cleared before parent tables
    cursor.execute("DELETE FROM transactions;")
    cursor.execute("DELETE FROM customers;")
    cursor.execute("DELETE FROM products;")

    print("Old database records cleared.")

    # Insert customers first
    cursor.executemany(
        customer_insert_query,
        customer_records
    )

    print("Customers inserted:", len(customer_records))

    # Insert products
    cursor.executemany(
        product_insert_query,
        product_records
    )

    print("Products inserted:", len(product_records))

    # Insert transactions last
    cursor.executemany(
        transaction_insert_query,
        records
    )

    print("Transactions inserted:", len(records))

    # Save database changes
    connection.commit()

    print("Database load completed successfully.")

    # Verify transaction count
    cursor.execute("SELECT COUNT(*) FROM transactions;")
    transaction_count = cursor.fetchone()[0]

    # Verify customer count
    cursor.execute("SELECT COUNT(*) FROM customers;")
    customer_count = cursor.fetchone()[0]

    # Verify product count
    cursor.execute("SELECT COUNT(*) FROM products;")
    product_count = cursor.fetchone()[0]

    print("Verified Transactions:", transaction_count)
    print("Verified Customers:", customer_count)
    print("Verified Products:", product_count)

    # Expected counts
    expected_transactions = len(records)
    expected_customers = len(customer_records)
    expected_products = len(product_records)

    # Validate database load
    if (
        transaction_count == expected_transactions
        and customer_count == expected_customers
        and product_count == expected_products
    ):
        print("Database validation passed.")
    else:
        print("Database validation failed.")

except Error as error:
    print("MySQL Error:", error)

    if connection is not None:
        connection.rollback()

except Exception as error:
    print("Pipeline Error:", error)

finally:
    if cursor is not None:
        cursor.close()

    if connection is not None and connection.is_connected():
        connection.close()

    print("Database resources closed.")