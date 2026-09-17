CREATE DATABASE IF NOT EXISTS ecommerce_analytics;

USE ecommerce_analytics;
CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(20) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR(20) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS transactions (
    order_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    product_id VARCHAR(20) NOT NULL,
    order_date DATE NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    unit_cost DECIMAL(10,2) NOT NULL,
    category VARCHAR(50),
    region VARCHAR(20),

    CONSTRAINT fk_transactions_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    CONSTRAINT fk_transactions_product
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);

-- Performance indexes are created separately after the initial data load.
-- See sql/performance_test.sql for query performance analysis.
