-- =========================================================
-- Performance Indexes — added after profiling the slow query
-- documented in full in benchmark_results.md
-- =========================================================
USE marketplace_db;

-- Composite index supporting the dashboard's most common filter pattern:
-- status + payment method + date range (in that selectivity order).
-- Before: full table scan on `orders`  (type: ALL)
-- After:  indexed range scan            (type: range)
CREATE INDEX idx_orders_status_payment_date
    ON orders(order_status, payment_method, order_date);

-- Supports GROUP BY / filtering on customer city without a full scan
-- + filesort on the customers table.
CREATE INDEX idx_customers_city
    ON customers(city);
