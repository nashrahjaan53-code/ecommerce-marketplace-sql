USE marketplace_db;

-- =========================================================
-- 1. Top 10 sellers by net revenue after commission
-- =========================================================
SELECT s.business_name,
       COUNT(DISTINCT oi.order_id) AS orders_fulfilled,
       SUM(oi.line_total) AS gross_revenue,
       SUM(c.commission_amount) AS commission_paid,
       SUM(oi.line_total) - SUM(c.commission_amount) AS net_seller_revenue
FROM order_items oi
JOIN sellers s ON oi.seller_id = s.seller_id
JOIN commissions c ON c.order_item_id = oi.order_item_id
GROUP BY s.seller_id, s.business_name
ORDER BY net_seller_revenue DESC
LIMIT 10;

-- =========================================================
-- 2. Category performance: revenue, avg rating, return rate
-- =========================================================
SELECT cat.category_name,
       COUNT(DISTINCT p.product_id) AS num_products,
       SUM(oi.line_total) AS category_revenue,
       ROUND(AVG(r.rating), 2) AS avg_rating,
       ROUND(100.0 * COUNT(DISTINCT ret.return_id) / NULLIF(COUNT(DISTINCT oi.order_item_id), 0), 2) AS return_rate_pct
FROM categories cat
JOIN products p ON p.category_id = cat.category_id
LEFT JOIN order_items oi ON oi.product_id = p.product_id
LEFT JOIN reviews r ON r.product_id = p.product_id
LEFT JOIN returns ret ON ret.order_item_id = oi.order_item_id
GROUP BY cat.category_id, cat.category_name
ORDER BY category_revenue DESC;

-- =========================================================
-- 3. Customer lifetime value tiers (percentile-based, RFM-style)
-- =========================================================
WITH customer_ltv AS (
    SELECT c.customer_id, COALESCE(SUM(o.total_amount), 0) AS lifetime_value
    FROM customers c
    LEFT JOIN orders o ON o.customer_id = c.customer_id AND o.order_status = 'delivered'
    GROUP BY c.customer_id
),
ranked AS (
    SELECT customer_id, lifetime_value,
           PERCENT_RANK() OVER (ORDER BY lifetime_value) AS pct_rank
    FROM customer_ltv
)
SELECT
    CASE
        WHEN pct_rank >= 0.80 THEN 'High Value (top 20%)'
        WHEN pct_rank >= 0.40 THEN 'Mid Value'
        ELSE 'Low Value (bottom 40%)'
    END AS customer_tier,
    COUNT(*) AS num_customers,
    ROUND(AVG(lifetime_value), 2) AS avg_ltv,
    ROUND(MIN(lifetime_value), 2) AS min_ltv,
    ROUND(MAX(lifetime_value), 2) AS max_ltv
FROM ranked
GROUP BY customer_tier
ORDER BY avg_ltv DESC;

-- =========================================================
-- 4. Monthly revenue trend with month-over-month % change
-- =========================================================
SELECT DATE_FORMAT(order_date, '%Y-%m') AS month,
       SUM(total_amount) AS monthly_revenue,
       ROUND(100.0 * (SUM(total_amount) - LAG(SUM(total_amount)) OVER (ORDER BY DATE_FORMAT(order_date, '%Y-%m')))
             / NULLIF(LAG(SUM(total_amount)) OVER (ORDER BY DATE_FORMAT(order_date, '%Y-%m')), 0), 2) AS mom_pct_change
FROM orders
WHERE order_status = 'delivered'
GROUP BY month
ORDER BY month;

-- =========================================================
-- 5. Products at risk of stockout (low stock, high demand)
-- =========================================================
SELECT p.product_name, p.stock_quantity,
       COUNT(oi.order_item_id) AS times_ordered,
       SUM(oi.quantity) AS total_units_sold
FROM products p
JOIN order_items oi ON oi.product_id = p.product_id
WHERE p.stock_quantity < 20
GROUP BY p.product_id, p.product_name, p.stock_quantity
HAVING total_units_sold > 10
ORDER BY total_units_sold DESC
LIMIT 15;
