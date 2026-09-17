import pandas as pd

# --------------------------------------------------
# 1. EXTRACT DATA
# --------------------------------------------------

df = pd.read_csv(
    "data/raw/ecommerce_transactions_50000.csv"
)

print("\nDataset Preview:")
print(df.head())

print("\nDataset Shape:", df.shape)
print("Columns:", df.columns.tolist())

raw_records = len(df)

print("\nRaw Records:", raw_records)


# --------------------------------------------------
# 2. DATA TYPE VALIDATION
# --------------------------------------------------

print("\nData Types:")
print(df.dtypes)

df["order_date"] = pd.to_datetime(
    df["order_date"],
    errors="coerce"
)

print("\nUpdated Data Types:")
print(df.dtypes)


# --------------------------------------------------
# 3. DATA QUALITY CHECKS
# --------------------------------------------------

print("\nMissing Values:")
print(df.isnull().sum())

duplicate_count = df.duplicated().sum()

print("\nDuplicate Rows:", duplicate_count)

invalid_rows = df[
    (df["quantity"] <= 0) |
    (df["unit_price"] <= 0) |
    (df["unit_cost"] < 0)
]

invalid_count = len(invalid_rows)

print("Invalid Rows:", invalid_count)

missing_critical_count = df[
    [
        "order_id",
        "customer_id",
        "product_id",
        "order_date"
    ]
].isnull().any(axis=1).sum()

print(
    "Missing Critical Records:",
    missing_critical_count
)


# --------------------------------------------------
# 4. CLEAN DATA
# --------------------------------------------------

# Remove duplicate records
df = df.drop_duplicates()

print("\nDuplicates removed.")

# Remove invalid transactions
df = df[
    (df["quantity"] > 0) &
    (df["unit_price"] > 0) &
    (df["unit_cost"] >= 0)
]

print("Invalid transactions removed.")

# Remove records with missing critical values
df = df.dropna(
    subset=[
        "order_id",
        "customer_id",
        "product_id",
        "order_date"
    ]
)

print("Missing critical records removed.")

# Reset DataFrame index after cleaning
df = df.reset_index(drop=True)

clean_records = len(df)
removed_records = raw_records - clean_records

print("\nRecords After Cleaning:", clean_records)
print("Records Removed:", removed_records)


# --------------------------------------------------
# 5. DATA INTEGRITY / RETENTION METRIC
# --------------------------------------------------

data_integrity = (
    clean_records / raw_records
) * 100

print(
    "Clean Data Integrity:",
    round(data_integrity, 2),
    "%"
)


# --------------------------------------------------
# 6. CALCULATE REVENUE
# --------------------------------------------------

df["revenue"] = (
    df["quantity"] *
    df["unit_price"]
)

print("\nRevenue calculated.")


# --------------------------------------------------
# 7. CALCULATE TOTAL COST
# --------------------------------------------------

df["total_cost"] = (
    df["quantity"] *
    df["unit_cost"]
)

print("Total cost calculated.")


# --------------------------------------------------
# 8. CALCULATE PROFIT
# --------------------------------------------------

df["profit"] = (
    df["revenue"] -
    df["total_cost"]
)

print("Profit calculated.")


# --------------------------------------------------
# 9. CALCULATE PROFIT MARGIN
# --------------------------------------------------

df["profit_margin_pct"] = (
    df["profit"] /
    df["revenue"] *
    100
).round(2)

print("Profit margin calculated.")


# --------------------------------------------------
# 10. BUSINESS SUMMARY
# --------------------------------------------------

total_revenue = df["revenue"].sum()
total_profit = df["profit"].sum()

print("\nTotal Revenue:", total_revenue)
print("Total Profit:", total_profit)


# --------------------------------------------------
# 11. CUSTOMER LIFETIME VALUE
# --------------------------------------------------

customer_clv = df.groupby(
    "customer_id"
).agg(
    total_orders=("order_id", "nunique"),
    total_revenue=("revenue", "sum"),
    total_profit=("profit", "sum")
).reset_index()

print(
    "\nCustomer Records:",
    len(customer_clv)
)


# --------------------------------------------------
# 12. PRODUCT SUMMARY
# --------------------------------------------------

product_summary = df.groupby(
    "product_id"
).agg(
    units_sold=("quantity", "sum"),
    total_revenue=("revenue", "sum"),
    total_profit=("profit", "sum")
).reset_index()

product_summary["profit_margin_pct"] = (
    product_summary["total_profit"] /
    product_summary["total_revenue"] *
    100
).round(2)

print(
    "Product Records:",
    len(product_summary)
)


# --------------------------------------------------
# 13. SAVE PROCESSED DATA
# --------------------------------------------------

df.to_csv(
    "data/processed/cleaned_transactions.csv",
    index=False
)

customer_clv.to_csv(
    "data/processed/customer_clv.csv",
    index=False
)

product_summary.to_csv(
    "data/processed/product_summary.csv",
    index=False
)

print("\nProcessed data saved successfully.")
print("Customer CLV saved successfully.")
print("Product summary saved successfully.")


# --------------------------------------------------
# 14. FINAL ETL SUMMARY
# --------------------------------------------------

print("\n========== ETL SUMMARY ==========")

print("Raw Records:", raw_records)
print("Duplicate Records Detected:", duplicate_count)
print("Invalid Records Detected:", invalid_count)
print(
    "Missing Critical Records Detected:",
    missing_critical_count
)
print("Records Removed:", removed_records)
print("Clean Records:", clean_records)

print(
    "Clean Data Integrity:",
    round(data_integrity, 2),
    "%"
)

print("=================================")
print("ETL pipeline completed successfully.")