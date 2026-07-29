"""
Benchmarks the city-revenue query described in benchmark_results.md.
Run with --before (pre-index) or --after (post-index) to log comparable timings.

Usage:
    python3 benchmark.py --before
    mysql marketplace_db < 02_indexes.sql
    python3 benchmark.py --after
"""

import argparse
import time
import mysql.connector

QUERY = """
SELECT c.city, COUNT(*) AS delivered_orders, SUM(o.total_amount) AS revenue,
       AVG(o.total_amount) AS avg_order_value
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
  AND o.payment_method = 'cod'
  AND o.order_date BETWEEN '2024-06-01' AND '2025-06-30'
GROUP BY c.city
ORDER BY revenue DESC
LIMIT 15;
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--before", action="store_true")
    parser.add_argument("--after", action="store_true")
    parser.add_argument("--runs", type=int, default=7)
    args = parser.parse_args()

    label = "BEFORE indexing" if args.before else "AFTER indexing" if args.after else "benchmark"

    conn = mysql.connector.connect(
        host="localhost", unix_socket="/run/mysqld/mysqld.sock",
        user="root", database="marketplace_db"
    )
    cur = conn.cursor()

    times = []
    for i in range(args.runs):
        t0 = time.perf_counter()
        cur.execute(QUERY)
        cur.fetchall()
        t1 = time.perf_counter()
        times.append((t1 - t0) * 1000)

    print(f"=== {label} ===")
    print("Individual run times (ms):", [round(t, 2) for t in times])
    print("Average (excl. first warm-up run):", round(sum(times[1:]) / len(times[1:]), 2), "ms")

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
