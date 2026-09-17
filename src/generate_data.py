import pandas as pd
import numpy as np

np.random.seed(42)

num_records = 50000

print("Records to generate:", num_records)
order_ids = [
    f"ORD{i:06d}"
    for i in range(1, num_records + 1)
]

print("First Order ID:", order_ids[0])
print("Last Order ID:", order_ids[-1])
customer_ids = np.random.randint(1, 5001, size=num_records)
customer_ids = [f"CUST{i:05d}" for i in customer_ids]

print("Sample Customers:", customer_ids[:5])
product_ids = np.random.randint(1, 501, size=num_records)
product_ids = [f"PROD{i:04d}" for i in product_ids]

print("Sample Products:", product_ids[:5])
dates = pd.date_range(
    start="2025-01-01",
    end="2025-12-31"
)

order_dates = np.random.choice(dates, size=num_records)

print("Sample Dates:", order_dates[:5])
quantities = np.random.randint(
    1,
    6,
    size=num_records
)

print("Sample Quantities:", quantities[:5])
categories = np.random.choice(
    ["Electronics", "Fashion", "Home", "Beauty", "Sports"],
    size=num_records
)
regions = np.random.choice(
    ["North", "South", "East", "West"],
    size=num_records
)
print("Sample Categories:", categories[:5])
print("Sample Regions:", regions[:5])
unit_prices = np.random.randint(
    200,
    5001,
    size=num_records
)

print("Sample Prices:", unit_prices[:5])
cost_percentages = np.random.uniform(
    0.50,
    0.85,
    size=num_records
)

unit_costs = (unit_prices * cost_percentages).astype(int)

print("Sample Costs:", unit_costs[:5])
df = pd.DataFrame({
    "order_id": order_ids,
    "customer_id": customer_ids,
    "product_id": product_ids,
    "order_date": order_dates,
    "quantity": quantities,
    "unit_price": unit_prices,
    "unit_cost": unit_costs,
    "category": categories,
    "region": regions
})
print("\nDataset Preview:")
print(df.head())
print("\nDataset Shape:", df.shape)

# Inject controlled data-quality issues for ETL testing
df.loc[0, "quantity"] = 0
df.loc[1, "unit_price"] = 0
df.loc[2, "unit_cost"] = -100
df.loc[3, "customer_id"] = None
df.loc[4, "product_id"] = None
duplicate_rows = df.iloc[[5, 6]].copy()

df = pd.concat(
    [df, duplicate_rows],
    ignore_index=True
)

print("Controlled dirty records added.")
print("Raw dataset rows:", len(df))

print(
    "\nSynthetic transaction dataset saved successfully:",
    len(df),
    "raw rows"
)