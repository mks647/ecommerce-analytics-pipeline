USE ecommerce_analytics;

-- Overall business performance
SELECT
    COUNT(*) AS total_transactions,
    ROUND(SUM(quantity * unit_price), 2) AS total_revenue,
    ROUND(SUM(quantity * (unit_price - unit_cost)), 2) AS total_profit
FROM transactions;
-- Top 10 customers by revenue
SELECT
    customer_id,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(quantity * unit_price), 2) AS total_revenue
FROM transactions
GROUP BY customer_id
ORDER BY total_revenue DESC
LIMIT 10;
-- Top 10 products by profit
SELECT
    product_id,
    SUM(quantity) AS units_sold,
    ROUND(SUM(quantity * unit_price), 2) AS total_revenue,
    ROUND(SUM(quantity * (unit_price - unit_cost)), 2) AS total_profit
FROM transactions
GROUP BY product_id
ORDER BY total_profit DESC
LIMIT 10;
-- Monthly revenue and profit trend
SELECT
    DATE_FORMAT(order_date, '%Y-%m') AS month,
    COUNT(*) AS total_transactions,
    ROUND(SUM(quantity * unit_price), 2) AS total_revenue,
    ROUND(SUM(quantity * (unit_price - unit_cost)), 2) AS total_profit
FROM transactions
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY month;