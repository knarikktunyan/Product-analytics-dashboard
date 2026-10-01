-- Regional performance
SELECT
    region,
    COUNT(*) AS orders,
    ROUND(SUM(revenue), 2) AS revenue
FROM orders
GROUP BY region
ORDER BY revenue DESC;
