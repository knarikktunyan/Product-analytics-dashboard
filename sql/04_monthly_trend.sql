-- Monthly revenue trend
SELECT
    strftime('%Y-%m', order_date) AS month,
    COUNT(*) AS orders,
    ROUND(SUM(revenue), 2) AS revenue
FROM orders
GROUP BY month
ORDER BY month;
