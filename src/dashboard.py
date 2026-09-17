import os

import mysql.connector
import pandas as pd
import streamlit as st
from dotenv import load_dotenv


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Business Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("Business Analytics Dashboard")

st.caption(
    "Analyze sales, revenue, profit, customers, "
    "products, categories, and regions."
)


# --------------------------------------------------
# ENVIRONMENT VARIABLES
# --------------------------------------------------

load_dotenv()


# --------------------------------------------------
# REQUIRED CLIENT DATA COLUMNS
# --------------------------------------------------

REQUIRED_COLUMNS = [
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


# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


# --------------------------------------------------
# LOAD DEMO DATABASE DATA
# --------------------------------------------------

@st.cache_data
def load_demo_data():
    connection = get_connection()

    query = """
    SELECT
        order_id,
        customer_id,
        product_id,
        order_date,
        quantity,
        unit_price,
        unit_cost,
        category,
        region
    FROM transactions
    """

    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return pd.DataFrame(rows)


# --------------------------------------------------
# VALIDATE CLIENT DATA
# --------------------------------------------------

def validate_client_data(dataframe):
    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in dataframe.columns
    ]

    if missing_columns:
        return False, missing_columns

    return True, []


# --------------------------------------------------
# CLEAN CLIENT DATA
# --------------------------------------------------

def clean_client_data(dataframe):
    dataframe = dataframe.copy()

    dataframe["order_date"] = pd.to_datetime(
        dataframe["order_date"],
        errors="coerce"
    )

    numeric_columns = [
        "quantity",
        "unit_price",
        "unit_cost"
    ]

    for column in numeric_columns:
        dataframe[column] = pd.to_numeric(
            dataframe[column],
            errors="coerce"
        )

    dataframe = dataframe.drop_duplicates()

    dataframe = dataframe.dropna(
        subset=REQUIRED_COLUMNS
    )

    dataframe = dataframe[
        (dataframe["quantity"] > 0)
        & (dataframe["unit_price"] > 0)
        & (dataframe["unit_cost"] >= 0)
    ]

    return dataframe.reset_index(drop=True)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header("Dashboard Controls")

data_source = st.sidebar.radio(
    "Choose Data Source",
    [
        "Upload My Data",
        "Demo Database"
    ]
)


# --------------------------------------------------
# SELECT DATA SOURCE
# --------------------------------------------------

df = None

if data_source == "Demo Database":

    st.sidebar.success(
        "Using demo database"
    )

    try:
        df = load_demo_data()

    except Exception as error:
        st.error(
            "Unable to load the demo database."
        )

        st.code(str(error))
        st.stop()


else:

    st.sidebar.info(
        "Upload a CSV file using the required format."
    )

    uploaded_file = st.sidebar.file_uploader(
        "Upload CSV",
        type=["csv"]
    )

    if uploaded_file is None:
        st.info(
            "Upload a CSV file to start the analysis."
        )

        st.write("Required columns:")

        st.code(
            ", ".join(REQUIRED_COLUMNS)
        )

        st.stop()

    try:
        uploaded_df = pd.read_csv(
            uploaded_file
        )

    except Exception:
        st.error(
            "The uploaded file could not be read as CSV."
        )
        st.stop()

    is_valid, missing_columns = (
        validate_client_data(uploaded_df)
    )

    if not is_valid:
        st.error(
            "The uploaded file is missing "
            "required columns."
        )

        st.write("Missing columns:")

        st.code(
            ", ".join(missing_columns)
        )

        st.stop()

    raw_uploaded_records = len(uploaded_df)

    df = clean_client_data(
        uploaded_df
    )

    removed_uploaded_records = (
        raw_uploaded_records - len(df)
    )

    if df.empty:
        st.error(
            "No valid transaction records remain "
            "after data validation."
        )
        st.stop()

    st.sidebar.success(
        "Client data loaded successfully"
    )

    st.sidebar.write(
        f"Uploaded rows: "
        f"{raw_uploaded_records:,}"
    )

    st.sidebar.write(
        f"Valid rows: {len(df):,}"
    )

    st.sidebar.write(
        f"Removed rows: "
        f"{removed_uploaded_records:,}"
    )


# --------------------------------------------------
# PREPARE ANALYTICS DATA
# --------------------------------------------------

df["order_date"] = pd.to_datetime(
    df["order_date"],
    errors="coerce"
)

numeric_columns = [
    "quantity",
    "unit_price",
    "unit_cost"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# Final safety validation
df = df.dropna(
    subset=REQUIRED_COLUMNS
)

df = df[
    (df["quantity"] > 0)
    & (df["unit_price"] > 0)
    & (df["unit_cost"] >= 0)
].copy()


# --------------------------------------------------
# CALCULATED METRICS
# --------------------------------------------------

df["revenue"] = (
    df["quantity"]
    * df["unit_price"]
)

df["total_cost"] = (
    df["quantity"]
    * df["unit_cost"]
)

df["profit"] = (
    df["revenue"]
    - df["total_cost"]
)

df["profit_margin_pct"] = (
    df["profit"]
    / df["revenue"]
    * 100
).round(2)


# --------------------------------------------------
# REFRESH BUTTON
# --------------------------------------------------

if st.sidebar.button(
    "Refresh Dashboard"
):
    st.cache_data.clear()
    st.rerun()


# --------------------------------------------------
# FILTER OPTIONS
# --------------------------------------------------

category_options = sorted(
    df["category"]
    .astype(str)
    .unique()
    .tolist()
)

region_options = sorted(
    df["region"]
    .astype(str)
    .unique()
    .tolist()
)

selected_categories = (
    st.sidebar.multiselect(
        "Category",
        category_options,
        default=category_options
    )
)

selected_regions = (
    st.sidebar.multiselect(
        "Region",
        region_options,
        default=region_options
    )
)


# --------------------------------------------------
# FILTER DATA
# --------------------------------------------------

filtered_df = df[
    df["category"]
    .astype(str)
    .isin(selected_categories)
    &
    df["region"]
    .astype(str)
    .isin(selected_regions)
].copy()


if filtered_df.empty:
    st.warning(
        "No records match the selected filters."
    )
    st.stop()


# --------------------------------------------------
# KPI CALCULATIONS
# --------------------------------------------------

total_revenue = (
    filtered_df["revenue"].sum()
)

total_profit = (
    filtered_df["profit"].sum()
)

total_orders = (
    filtered_df["order_id"].nunique()
)

total_customers = (
    filtered_df["customer_id"].nunique()
)

profit_margin = (
    (total_profit / total_revenue) * 100
    if total_revenue > 0
    else 0
)


# --------------------------------------------------
# KPI DISPLAY
# --------------------------------------------------

st.subheader("Business Overview")

col1, col2, col3, col4, col5 = (
    st.columns(5)
)

col1.metric(
    "Total Revenue",
    f"₹{total_revenue:,.0f}"
)

col2.metric(
    "Total Profit",
    f"₹{total_profit:,.0f}"
)

col3.metric(
    "Profit Margin",
    f"{profit_margin:.2f}%"
)

col4.metric(
    "Orders",
    f"{total_orders:,}"
)

col5.metric(
    "Customers",
    f"{total_customers:,}"
)


# --------------------------------------------------
# CATEGORY AND REGION ANALYTICS
# --------------------------------------------------

left_column, right_column = (
    st.columns(2)
)

with left_column:

    st.subheader(
        "Revenue by Category"
    )

    category_revenue = (
        filtered_df
        .groupby("category")["revenue"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    st.bar_chart(
        category_revenue,
        width="stretch"
    )


with right_column:

    st.subheader(
        "Profit by Region"
    )

    region_profit = (
        filtered_df
        .groupby("region")["profit"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    st.bar_chart(
        region_profit,
        width="stretch"
    )


# --------------------------------------------------
# MONTHLY REVENUE
# --------------------------------------------------

st.subheader(
    "Monthly Revenue Trend"
)

monthly_revenue = (
    filtered_df
    .set_index("order_date")
    .resample("ME")["revenue"]
    .sum()
)

st.line_chart(
    monthly_revenue,
    width="stretch"
)


# --------------------------------------------------
# CUSTOMER ANALYTICS
# --------------------------------------------------

st.subheader(
    "Top Customers by Lifetime Value"
)

customer_clv = (
    filtered_df
    .groupby("customer_id")
    .agg(
        total_orders=(
            "order_id",
            "nunique"
        ),
        total_revenue=(
            "revenue",
            "sum"
        ),
        total_profit=(
            "profit",
            "sum"
        )
    )
    .reset_index()
    .sort_values(
        "total_revenue",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    customer_clv,
    width="stretch",
    hide_index=True
)


# --------------------------------------------------
# PRODUCT ANALYTICS
# --------------------------------------------------

st.subheader(
    "Top Products by Profit"
)

product_summary = (
    filtered_df
    .groupby("product_id")
    .agg(
        units_sold=(
            "quantity",
            "sum"
        ),
        total_revenue=(
            "revenue",
            "sum"
        ),
        total_profit=(
            "profit",
            "sum"
        )
    )
    .reset_index()
)

product_summary[
    "profit_margin_pct"
] = (
    product_summary["total_profit"]
    / product_summary["total_revenue"]
    * 100
).round(2)

product_summary = (
    product_summary
    .sort_values(
        "total_profit",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    product_summary,
    width="stretch",
    hide_index=True
)


# --------------------------------------------------
# TRANSACTION PREVIEW
# --------------------------------------------------

st.subheader(
    "Transaction Data Preview"
)

st.write(
    f"Analyzing "
    f"{len(filtered_df):,} "
    f"transaction records."
)

st.dataframe(
    filtered_df.head(100),
    width="stretch",
    hide_index=True
)


# --------------------------------------------------
# PRIVACY MESSAGE
# --------------------------------------------------

if data_source == "Upload My Data":

    st.info(
        "Uploaded CSV data is used for "
        "the current dashboard analysis "
        "and is not written to the "
        "project MySQL database."
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Analytics Pipeline: "
    "Python | Pandas | MySQL | Streamlit"
)