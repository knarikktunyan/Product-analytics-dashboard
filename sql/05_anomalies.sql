-- Flag unusually large orders
WITH stats AS (
    SELECT AVG(revenue) AS avg_revenue,
           AVG(revenue * revenue) AS avg_square
    FROM orders
)
SELECT
    order_id,
    order_date,
    product,
    region,
    revenue
FROM orders, stats
WHERE revenue > avg_revenue + 2 * sqrt(avg_square - avg_revenue * avg_revenue)
ORDER BY revenue DESC;
