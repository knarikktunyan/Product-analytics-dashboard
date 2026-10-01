-- Main KPIs
SELECT
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(AVG(revenue), 2) AS avg_order_value,
    SUM(quantity) AS units_sold
FROM orders;
