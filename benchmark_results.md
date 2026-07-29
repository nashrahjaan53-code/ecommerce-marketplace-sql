# Query Performance Benchmark

Every number below was measured directly against the live dataset (50,000 orders, 8,000 customers, 294K+ total rows) — not estimated. Methodology, raw output, and how to reproduce it are all included.

## The problem query

A city-level revenue dashboard needs to answer: *"For delivered, COD orders in the last year, what's the order count, revenue, and average order value per city?"*

```sql
SELECT c.city,
       COUNT(*) AS delivered_orders,
       SUM(o.total_amount) AS revenue,
       AVG(o.total_amount) AS avg_order_value
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
  AND o.payment_method = 'cod'
  AND o.order_date BETWEEN '2024-06-01' AND '2025-06-30'
GROUP BY c.city
ORDER BY revenue DESC
LIMIT 15;
```

`orders.order_status`, `orders.payment_method`, `orders.order_date`, and `customers.city` had **no indexes** at the start — only primary keys and the auto-created foreign-key index on `customer_id`.

## Before indexing

**EXPLAIN plan:**

| table | type | key | rows examined | Extra |
|---|---|---|---|---|
| `customers` | **ALL** (full table scan) | — | 8,000 | Using temporary; Using filesort |
| `orders` | ref | customer_id | ~3 per customer | Using where |

The full scan + filesort on `customers` is the bottleneck — MySQL has no way to filter or pre-sort by city without reading every row.

**Measured execution time** (Python `mysql-connector`, `time.perf_counter()`, 7 runs, first run discarded as warm-up):

```
Individual runs (ms): [118.37, 89.98, 91.11, 90.07, 93.39, 99.91, 95.99]
Average: 93.41 ms
```

## The fix

```sql
CREATE INDEX idx_orders_status_payment_date
    ON orders(order_status, payment_method, order_date);

CREATE INDEX idx_customers_city
    ON customers(city);
```

Column order in the composite index matches selectivity: `order_status` (5 values) → `payment_method` (5 values) → `order_date` (range scan on the most granular column last, which is the correct pattern for range-scan-friendly composite indexes).

## After indexing

**EXPLAIN plan:**

| table | type | key | rows examined | Extra |
|---|---|---|---|---|
| `orders` | **range** | idx_orders_status_payment_date | 2,120 | Using index condition; Using temporary; Using filesort |
| `customers` | eq_ref | PRIMARY | 1 | — |

`orders` went from a `ref` scan feeding off a full customer scan, to a `range` scan hitting the new composite index directly — and `customers` now does a 1-row primary-key lookup (`eq_ref`) instead of reading all 8,000 rows.

**Measured execution time** (same methodology, 7 runs):

```
Individual runs (ms): [11.80, 12.15, 13.88, 10.35, 10.34, 9.95, 10.15]
Average: 11.14 ms
```

## Result

| | Before | After | Change |
|---|---|---|---|
| Avg execution time | 93.41 ms | 11.14 ms | **8.4x faster** |
| Customers table scan | 8,000 rows (ALL) | 1 row (eq_ref) | — |
| Orders table access | ref + filter | range (index) | — |

## How to reproduce

```bash
mysql marketplace_db < 01_schema.sql
python3 generate_data.py          # writes CSVs to /data
# load CSVs via LOAD DATA LOCAL INFILE (see load_data.sql)
python3 benchmark.py --before      # run before creating indexes
mysql marketplace_db < 02_indexes.sql
python3 benchmark.py --after       # run again after
```

*Environment: MariaDB 10.11, single-node, default InnoDB buffer pool settings — no tuning beyond the indexes shown above.*
