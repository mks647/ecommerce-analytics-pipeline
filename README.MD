# E-Commerce Analytics Pipeline & Business Dashboard

An end-to-end data analytics solution that transforms raw transaction data into validated business insights through an interactive web dashboard.

The application allows users to explore demo business data or upload their own CSV file to automatically generate sales, revenue, profit, customer, product, category, regional, and monthly analytics.

---

## Live Demo

Try the application here:

**LIVE_DEMO_URL_HERE**

No local installation is required to test the deployed dashboard.

---

## What This Project Does

The solution provides an end-to-end analytics workflow:

Raw Transaction Data  
→ Data Validation  
→ Data Cleaning  
→ Business Metric Calculation  
→ Analytics Processing  
→ Interactive Dashboard

The project includes Python-based ETL processing, MySQL database integration, SQL analytics, data-quality validation, and a Streamlit web dashboard.

---

## Client Testing

A client can test the dashboard without installing Python or MySQL.

### Option 1: Demo Data

Select:

`Demo Database`

The application loads the prepared demo transaction dataset and generates the complete analytics dashboard.

### Option 2: Upload Your Own Data

Select:

`Upload My Data`

Then:

1. Click **Download Sample CSV**.
2. Review the required data format.
3. Replace the sample rows with your own business transaction data.
4. Upload the CSV file.
5. The application validates and cleans the uploaded records.
6. The dashboard automatically generates business analytics.

Uploaded CSV test data is processed for dashboard analysis and is not automatically written to the project MySQL database.

---

## Required CSV Format

The uploaded CSV must contain these columns:

| Column | Description |
|---|---|
| `order_id` | Unique transaction/order identifier |
| `customer_id` | Customer identifier |
| `product_id` | Product identifier |
| `order_date` | Transaction date |
| `quantity` | Number of units sold |
| `unit_price` | Selling price per unit |
| `unit_cost` | Cost per unit |
| `category` | Product category |
| `region` | Sales region |

A ready-to-use template is available inside:

`sample_data/client_sample.csv`

---

## Dashboard Analytics

The dashboard provides:

- Total Revenue
- Total Profit
- Overall Profit Margin
- Total Orders
- Total Customers
- Revenue by Category
- Profit by Region
- Monthly Revenue Trend
- Customer Lifetime Value analysis
- Top Customers by Revenue
- Product Profitability
- Product Profit Margins
- Transaction Data Preview
- Category and Region Filters

---

## Data Validation

Uploaded transaction data is validated before analytics are generated.

The pipeline handles:

- Duplicate records
- Missing critical values
- Invalid dates
- Invalid numeric values
- Zero or negative quantities
- Zero or negative selling prices
- Negative unit costs

Invalid records are removed from the analytics dataset according to the validation rules.

---

## Dataset

The project starts with 50,000 synthetic e-commerce transactions.

Controlled data-quality test records were introduced to test ETL validation.

Pipeline results:

- Base synthetic transactions: 50,000
- Raw records after controlled test cases: 50,002
- Duplicate records detected: 2
- Invalid transaction records detected: 3
- Missing-critical records detected: 2
- Records removed: 7
- Final cleaned records: 49,995
- Raw-to-clean record retention: approximately 99.99%

These are project test metrics generated from the synthetic dataset.

---

## Business Metrics

Revenue:

`Revenue = Quantity × Unit Price`

Total Cost:

`Total Cost = Quantity × Unit Cost`

Profit:

`Profit = Revenue - Total Cost`

Profit Margin:

`Profit Margin (%) = (Profit / Revenue) × 100`

Customer analytics aggregate historical orders, revenue, and profit by customer.

---

## Technology Stack

- Python
- Pandas
- NumPy
- MySQL
- SQL
- Streamlit
- Git
- GitHub
- Streamlit Community Cloud

---

## Project Structure

```text
ecommerce-analytics-pipeline/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── sample_data/
│   └── client_sample.csv
│
├── sql/
│   ├── schema.sql
│   ├── analytics_queries.sql
│   ├── data_quality.sql
│   └── performance_test.sql
│
├── src/
│   ├── generate_data.py
│   ├── extract.py
│   ├── db_connection.py
│   └── dashboard.py
│
├── .gitignore
├── README.MD
└── requirements.txt
```

---

## ETL Pipeline

### 1. Extract

Transaction data is loaded from the raw CSV dataset.

### 2. Validate

The pipeline checks data types, missing critical values, duplicate records, and invalid transaction values.

### 3. Transform

The pipeline calculates:

- Revenue
- Total Cost
- Profit
- Profit Margin
- Customer-level analytics
- Product-level analytics

### 4. Load

Validated transaction records can be loaded into the relational MySQL database.

### 5. Analyze

SQL queries provide customer, product, category, regional, profitability, and time-based analysis.

### 6. Visualize

The Streamlit dashboard converts the processed data into interactive business analytics.

---

## Database Design

The MySQL implementation uses:

- `customers`
- `products`
- `transactions`

Primary and foreign-key relationships maintain relational integrity.

SQL indexing and `EXPLAIN ANALYZE` are used for query-performance testing.

---

## Local Installation

Clone the repository:

```bash
git clone https://github.com/mks647/ecommerce-analytics-pipeline.git
cd ecommerce-analytics-pipeline
```

Create a virtual environment:

```bash
python -m venv .venv
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Configuration

Create a local `.env` file:

```text
DB_HOST=localhost
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_NAME=ecommerce_analytics
```

The `.env` file is excluded from Git version control and should never be committed to the public repository.

---

## Run the ETL Pipeline

Generate synthetic data:

```bash
python src/generate_data.py
```

Run data cleaning and transformation:

```bash
python src/extract.py
```

Load validated data into MySQL:

```bash
python src/db_connection.py
```

---

## Run the Dashboard Locally

```bash
streamlit run src/dashboard.py
```

Then open the local Streamlit address shown in the terminal.

---

## Deployment

The client-facing dashboard is deployed as a web application.

Users can access the application through the live demo URL without installing the development environment.

For client demonstrations, the application supports CSV-based testing directly through the browser.

---

## Client Customization

The analytics solution can be adapted for different businesses by customizing:

- Company branding
- Business-specific KPIs
- Product attributes
- Sales fields
- Inventory fields
- Customer metrics
- Regional reporting
- Dashboard charts
- Data-source integrations

For example, the same analytics architecture can be adapted for retail, tiles, manufacturing, wholesale, or other transaction-based businesses.

---

## Security

Sensitive database credentials are stored outside the Git repository using environment variables.

Client test uploads are analyzed by the dashboard and are not automatically inserted into the project MySQL database.

Production deployments should use client-specific authentication, database infrastructure, access controls, backup policies, and data-retention rules based on business requirements.

---

## Purpose

This project demonstrates an end-to-end analytics workflow covering data generation, ETL, data-quality validation, relational database design, SQL analytics, performance testing, interactive visualization, client-data testing, and cloud deployment.