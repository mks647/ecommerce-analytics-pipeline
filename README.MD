# E-Commerce Analytics Pipeline

An end-to-end data engineering and analytics project that generates, cleans, validates, transforms, and loads 50,000 synthetic e-commerce transaction records into MySQL for business analytics.
## Project Objective

The goal of this project is to build a reproducible ETL pipeline for e-commerce transaction data and generate insights related to revenue, profit, customers, products, and regional performance.
## Tech Stack

- Python
- Pandas
- NumPy
- MySQL
- MySQL Workbench
- python-dotenv

## ETL Workflow

1. Generate 50,000 synthetic e-commerce transactions.
2. Extract transaction data using Pandas.
3. Validate missing, duplicate, and invalid records.
4. Clean and transform the dataset.
5. Calculate revenue, cost, profit, and profit margins.
6. Generate customer and product-level aggregations.
7. Load cleaned transaction data into MySQL.
8. Validate database records using SQL.
9. Perform customer, product, regional, and monthly analytics.
10. Optimize analytical queries using database indexes.

## Dataset

The project uses a reproducible synthetic e-commerce dataset containing:

- 50,000 transactions
- 5,000 unique customers
- 500 unique products
- 5 product categories
- 4 sales regions
- Transaction data covering the year 2025

## Project Structure

ecommerce-analytics-pipeline/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── sql/
│   ├── schema.sql
│   ├── analytics_queries.sql
│   └── performance_test.sql
├── src/
│   ├── generate_data.py
│   ├── extract.py
│   └── db_connection.py
├── .gitignore
├── requirements.txt
└── README.md

## Database Design

The MySQL database separates core entities into customer, product, and transaction tables.

- `customers` stores unique customer identifiers.
- `products` stores unique product identifiers.
- `transactions` stores transactional information.
- Foreign keys connect transactions with customers and products.
customers ──┐
            ├── transactions
products ───┘

## Calculated Metrics

The ETL and analytics workflow calculates:

- Revenue
- Total Cost
- Profit
- Profit Margin
- Customer Lifetime Revenue and Profit
- Product Revenue and Profit
- Regional Performance
- Monthly Revenue and Profit Trends

## SQL Analytics

The project includes SQL queries for:

- Overall revenue and profit
- Top customers by revenue
- Top products by revenue and profit
- Product profit margins
- Revenue by category
- Profit by region
- Monthly business trends
- Data quality validation
- Query execution analysis using `EXPLAIN ANALYZE`

## Security

Database credentials are stored in environment variables using a `.env` file and loaded with `python-dotenv`.

The `.env` file and virtual environment are excluded from version control using `.gitignore`.

## Installation

Clone the repository and navigate to the project directory:

```bash
git clone <repository-url>
cd ecommerce-analytics-pipeline
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```
## Environment Configuration

Create a `.env` file in the project root directory:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=ecommerce_analytics
```

Never commit the `.env` file to version control.
## Database Setup

Create the MySQL database:

```sql
CREATE DATABASE ecommerce_analytics;
USE ecommerce_analytics;
```

Run the SQL schema provided in:

```text
sql/schema.sql
```
## Running the Pipeline

Generate the synthetic dataset:

```bash
python src/generate_data.py
```

Run the ETL process:

```bash
python src/extract.py
```

Load the processed data into MySQL:

```bash
python src/db_connection.py
```
## Running the Analytics

After loading the data into MySQL, run the queries available in:

```text
sql/analytics_queries.sql
```

Query execution plans and performance tests are available in:

```text
sql/performance_test.sql
```
