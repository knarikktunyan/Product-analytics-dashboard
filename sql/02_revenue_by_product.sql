-- Revenue and orders by product
SELECT
    product,
    COUNT(*) AS orders,
    SUM(quantity) AS units_sold,
    ROUND(SUM(revenue), 2) AS revenue
FROM orders
GROUP BY product
ORDER BY revenue DESC;
