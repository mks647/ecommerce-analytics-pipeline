USE ecommerce_analytics;

-- ==================================================
-- E-Commerce Analytics Pipeline
-- SQL Performance Benchmark
-- ==================================================

-- Check existing indexes
SHOW INDEX FROM transactions;


-- ==================================================
-- BASELINE TEST
-- Run after removing idx_order_date
-- ==================================================

-- DROP INDEX idx_order_date
-- ON transactions;

EXPLAIN ANALYZE
SELECT
    order_id,
    customer_id,
    product_id,
    order_date,
    quantity,
    unit_price,
    unit_cost
FROM transactions
WHERE order_date >= '2025-06-01'
  AND order_date < '2025-07-01'
ORDER BY order_date;


-- ==================================================
-- CREATE PERFORMANCE INDEX
-- ==================================================

-- CREATE INDEX idx_order_date
-- ON transactions(order_date);


-- ==================================================
-- OPTIMIZED TEST
-- Run after creating idx_order_date
-- ==================================================

EXPLAIN ANALYZE
SELECT
    order_id,
    customer_id,
    product_id,
    order_date,
    quantity,
    unit_price,
    unit_cost
FROM transactions
WHERE order_date >= '2025-06-01'
  AND order_date < '2025-07-01'
ORDER BY order_date;
-- ==================================================
-- BENCHMARK RESULTS
-- ==================================================

-- Dataset: 49,995 cleaned transactions
-- Filter: June 2025
-- Matching rows: 4,188
--
-- Without order_date index:
-- EXPLAIN ANALYZE observed time: approximately 90.8 ms
--
-- With order_date index:
-- Pending final measured result
--
-- Performance improvement:
-- Pending final calculation