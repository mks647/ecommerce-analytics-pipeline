USE ecommerce_analytics;
-- Check total records and missing critical values
SELECT
    COUNT(*) AS total_records,
    SUM(customer_id IS NULL) AS missing_customers,
    SUM(product_id IS NULL) AS missing_products,
    SUM(order_date IS NULL) AS missing_dates
FROM transactions;
-- Check invalid transaction values
SELECT
    COUNT(*) AS invalid_records
FROM transactions
WHERE quantity <= 0
   OR unit_price <= 0
   OR unit_cost < 0;

   -- Check duplicate order IDs
SELECT
    order_id,
    COUNT(*) AS duplicate_count
FROM transactions
GROUP BY order_id
HAVING COUNT(*) > 1;

-- Calculate valid record percentage
SELECT
    COUNT(*) AS total_records,
    SUM(
        CASE
            WHEN customer_id IS NOT NULL
             AND product_id IS NOT NULL
             AND order_date IS NOT NULL
             AND quantity > 0
             AND unit_price > 0
             AND unit_cost >= 0
            THEN 1
            ELSE 0
        END
    ) AS valid_records,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN customer_id IS NOT NULL
                 AND product_id IS NOT NULL
                 AND order_date IS NOT NULL
                 AND quantity > 0
                 AND unit_price > 0
                 AND unit_cost >= 0
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS data_quality_pct
FROM transactions;