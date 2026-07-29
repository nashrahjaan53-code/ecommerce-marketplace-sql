"""
Generates realistic synthetic data for the marketplace_db schema and writes
CSV files ready for LOAD DATA INFILE / bulk insert.

Target scale:
  customers   : 8,000
  sellers     : 600
  categories  : 15
  products    : 12,000
  orders      : 50,000
  order_items : ~95,000  (1-3 items per order)
  reviews     : 20,000
  returns     : 4,000
  commissions : ~95,000  (one per order_item)

Total rows generated: ~280,000+
"""

import csv
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

OUT = "/home/claude/marketplace/data"
import os
os.makedirs(OUT, exist_ok=True)

CATEGORY_NAMES = [
    "Electronics", "Home & Kitchen", "Fashion", "Beauty & Personal Care",
    "Sports & Outdoors", "Books", "Toys & Games", "Automotive",
    "Grocery", "Health & Wellness", "Office Supplies", "Pet Supplies",
    "Furniture", "Jewelry", "Garden & Outdoor"
]

PAYMENT_METHODS = ["card", "upi", "netbanking", "cod", "wallet"]
ORDER_STATUSES = ["placed", "shipped", "delivered", "cancelled", "returned"]
# weighted so "delivered" dominates, like a real store
STATUS_WEIGHTS = [0.05, 0.10, 0.70, 0.08, 0.07]

def random_date(start_year=2023, end_year=2026):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 7, 1)
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

# ---------------------------------------------------------
# Categories
# ---------------------------------------------------------
with open(f"{OUT}/categories.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["category_id", "category_name"])
    for i, name in enumerate(CATEGORY_NAMES, start=1):
        w.writerow([i, name])

print("categories.csv written:", len(CATEGORY_NAMES))

# ---------------------------------------------------------
# Customers
# ---------------------------------------------------------
N_CUSTOMERS = 8000
with open(f"{OUT}/customers.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["customer_id", "full_name", "email", "city", "country", "signup_date"])
    for i in range(1, N_CUSTOMERS + 1):
        w.writerow([
            i, fake.name(), f"cust{i}_{fake.user_name()}@{fake.free_email_domain()}",
            fake.city(), fake.country(), random_date().date()
        ])
print("customers.csv written:", N_CUSTOMERS)

# ---------------------------------------------------------
# Sellers
# ---------------------------------------------------------
N_SELLERS = 600
with open(f"{OUT}/sellers.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["seller_id", "business_name", "email", "city", "country", "joined_date", "rating"])
    for i in range(1, N_SELLERS + 1):
        w.writerow([
            i, fake.company(), f"seller{i}_{fake.user_name()}@{fake.free_email_domain()}",
            fake.city(), fake.country(), random_date().date(), round(random.uniform(2.5, 5.0), 2)
        ])
print("sellers.csv written:", N_SELLERS)

# ---------------------------------------------------------
# Products
# ---------------------------------------------------------
N_PRODUCTS = 12000
with open(f"{OUT}/products.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["product_id", "seller_id", "category_id", "product_name", "price", "stock_quantity", "created_at"])
    for i in range(1, N_PRODUCTS + 1):
        w.writerow([
            i, random.randint(1, N_SELLERS), random.randint(1, len(CATEGORY_NAMES)),
            fake.catch_phrase(), round(random.uniform(4.99, 899.99), 2),
            random.randint(0, 500), random_date().date()
        ])
print("products.csv written:", N_PRODUCTS)

# ---------------------------------------------------------
# Orders + Order Items + Commissions (generated together for consistency)
# ---------------------------------------------------------
N_ORDERS = 50000
COMMISSION_RATE = 0.12  # flat 12% platform commission for simplicity

orders_f = open(f"{OUT}/orders.csv", "w", newline="", encoding="utf-8")
items_f = open(f"{OUT}/order_items.csv", "w", newline="", encoding="utf-8")
comm_f = open(f"{OUT}/commissions.csv", "w", newline="", encoding="utf-8")

orders_w = csv.writer(orders_f)
items_w = csv.writer(items_f)
comm_w = csv.writer(comm_f)

orders_w.writerow(["order_id", "customer_id", "order_date", "order_status", "payment_method", "total_amount"])
items_w.writerow(["order_item_id", "order_id", "product_id", "seller_id", "quantity", "unit_price", "line_total"])
comm_w.writerow(["commission_id", "order_item_id", "seller_id", "commission_rate", "commission_amount"])

item_id_counter = 1
comm_id_counter = 1

# Pre-load product price/seller lookup in memory to avoid re-reading the csv
products_lookup = []
with open(f"{OUT}/products.csv", "r", encoding="utf-8") as pf:
    reader = csv.DictReader(pf)
    for row in reader:
        products_lookup.append((int(row["product_id"]), int(row["seller_id"]), float(row["price"])))

for order_id in range(1, N_ORDERS + 1):
    customer_id = random.randint(1, N_CUSTOMERS)
    order_date = random_date()
    status = random.choices(ORDER_STATUSES, weights=STATUS_WEIGHTS, k=1)[0]
    payment = random.choice(PAYMENT_METHODS)

    n_items = random.randint(1, 3)
    order_total = 0.0
    chosen_items = random.sample(products_lookup, n_items)

    for (product_id, seller_id, price) in chosen_items:
        qty = random.randint(1, 4)
        line_total = round(price * qty, 2)
        order_total += line_total

        items_w.writerow([item_id_counter, order_id, product_id, seller_id, qty, price, line_total])

        commission_amount = round(line_total * COMMISSION_RATE, 2)
        comm_w.writerow([comm_id_counter, item_id_counter, seller_id, COMMISSION_RATE, commission_amount])

        item_id_counter += 1
        comm_id_counter += 1

    orders_w.writerow([order_id, customer_id, order_date, status, payment, round(order_total, 2)])

    if order_id % 10000 == 0:
        print(f"...generated {order_id} orders")

orders_f.close()
items_f.close()
comm_f.close()
print("orders.csv written:", N_ORDERS)
print("order_items.csv written:", item_id_counter - 1)
print("commissions.csv written:", comm_id_counter - 1)

# ---------------------------------------------------------
# Reviews
# ---------------------------------------------------------
N_REVIEWS = 20000
review_snippets = [
    "Great quality for the price.", "Not what I expected, quite disappointed.",
    "Fast shipping and good packaging.", "Works exactly as described.",
    "Would buy again.", "Item arrived damaged.", "Excellent value for money.",
    "Customer service was helpful.", "Average product, does the job.",
    "Exceeded my expectations!"
]
with open(f"{OUT}/reviews.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["review_id", "product_id", "customer_id", "rating", "review_text", "review_date"])
    for i in range(1, N_REVIEWS + 1):
        w.writerow([
            i, random.randint(1, N_PRODUCTS), random.randint(1, N_CUSTOMERS),
            random.randint(1, 5), random.choice(review_snippets), random_date().date()
        ])
print("reviews.csv written:", N_REVIEWS)

# ---------------------------------------------------------
# Returns (subset of order_items)
# ---------------------------------------------------------
N_RETURNS = 4000
return_reasons = ["Wrong size", "Item defective", "Changed my mind", "Arrived damaged", "Not as described"]
with open(f"{OUT}/returns.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["return_id", "order_item_id", "return_reason", "return_date", "refund_amount"])
    sampled_items = random.sample(range(1, item_id_counter), N_RETURNS)
    for i, oi_id in enumerate(sampled_items, start=1):
        w.writerow([
            i, oi_id, random.choice(return_reasons), random_date().date(),
            round(random.uniform(4.99, 500.00), 2)
        ])
print("returns.csv written:", N_RETURNS)

total_rows = (len(CATEGORY_NAMES) + N_CUSTOMERS + N_SELLERS + N_PRODUCTS +
              N_ORDERS + (item_id_counter - 1) + (comm_id_counter - 1) +
              N_REVIEWS + N_RETURNS)
print(f"\nTOTAL ROWS GENERATED: {total_rows:,}")
