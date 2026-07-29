# 🛒 E-Commerce Multi-Seller Marketplace
### SQL Analytics, Performance Engineering & Business Intelligence Platform

![MySQL](https://img.shields.io/badge/Database-MySQL-blue?style=for-the-badge&logo=mysql)
![Python](https://img.shields.io/badge/Python-Faker-green?style=for-the-badge&logo=python)
![Analytics](https://img.shields.io/badge/Focus-SQL%20Analytics-orange?style=for-the-badge)
![Performance](https://img.shields.io/badge/Performance%20Tuning-8.4x%20Speedup-red?style=for-the-badge)

---

## 📖 Project Overview

This project simulates a production-scale **multi-vendor e-commerce marketplace** where thousands of customers purchase products from hundreds of independent sellers.

Unlike traditional SQL portfolio projects that focus solely on schema design and CRUD operations, this repository emphasizes:

- Enterprise-scale relational modeling
- Business intelligence analytics
- Query optimization
- Performance engineering
- Benchmark-driven indexing strategies

The platform processes nearly **300,000 records** across customers, sellers, products, transactions, reviews, commissions, and returns, providing a realistic environment for advanced SQL analysis.

---

## 🎯 Business Objectives

The project answers critical business questions such as:

- Which sellers generate the highest net revenue?
- Which product categories drive marketplace growth?
- Who are the most valuable customers?
- Which products are at risk of stockouts?
- How are revenues trending month-over-month?
- How can slow dashboard queries be optimized?

---

## 🏗️ System Architecture

```text
Customers
    │
    ▼
Orders ─────► Order Items
    │              │
    ▼              ▼
Returns      Products ─────► Categories
    │              │
    ▼              ▼
Reviews      Sellers
                    │
                    ▼
              Commissions
```

---

## 📊 Dataset Scale

| Table | Rows |
|---|---:|
| Customers | 8,000 |
| Sellers | 600 |
| Products | 12,000 |
| Orders | 50,000 |
| Order Items | 99,908 |
| Commissions | 99,908 |
| Reviews | 20,000 |
| Returns | 4,000 |
| Categories | 15 |
| **Total Records** | **294,431** |

---

## ⚡ Performance Engineering Case Study

One of the primary goals of this project was to demonstrate real-world SQL optimization.

### Initial State

A seller-performance dashboard query required:

- Full table scans
- Large intermediate result sets
- Excessive row reads

**Execution Time:** 93 ms

---

### Optimization Strategy

Implemented:

- Composite indexing
- Query plan analysis using `EXPLAIN`
- Join optimization
- Index coverage improvements

---

### Final Result

| Metric | Before | After |
|---|---:|---:|
| Execution Time | 93 ms | 11 ms |
| Improvement | — | **8.4x Faster** |

✅ Full benchmark methodology available in:

```text
benchmark_results.md
```

Including:

- Raw benchmark runs
- Query plans
- EXPLAIN output
- Index rationale
- Reproducibility steps

---

## 📈 Advanced SQL Concepts Demonstrated

### Window Functions

```sql
PERCENT_RANK()
LAG()
ROW_NUMBER()
RANK()
DENSE_RANK()
```

Used for:

- Customer segmentation
- Revenue ranking
- Trend analysis
- Percentile calculations

---

### Common Table Expressions (CTEs)

```sql
WITH revenue_summary AS (...)
```

Used for:

- Readable analytics pipelines
- Modular reporting logic
- Complex aggregations

---

### Query Optimization

- Composite indexes
- Covering indexes
- Execution plan analysis
- Benchmarking methodology
- Join optimization

---

## 📊 Business Intelligence Queries

### Seller Revenue Analytics

Identify:

- Top-performing sellers
- Net revenue after commission
- Marketplace concentration

---

### Customer Lifetime Value (LTV)

Segment customers using:

```sql
PERCENT_RANK()
```

instead of arbitrary spending thresholds.

---

### Revenue Trend Analysis

Month-over-month revenue tracking using:

```sql
LAG()
```

for growth calculations.

---

### Product Performance

Identify:

- Best-selling products
- Category leaders
- Inventory turnover patterns

---

### Stockout Risk Detection

Detect products with:

- Low inventory
- High historical sales velocity

before revenue loss occurs.

---

## 🔍 Key Insights

### 🏆 Top Marketplace Seller

**Wilson PLC**

- ₹312,916 net revenue
- 264 completed orders

---

### 💰 Customer Segmentation

The highest-spending 20% of customers generate approximately **4x more revenue** than the bottom 40%.

This percentile-based approach reveals purchasing patterns that fixed spending thresholds fail to capture.

---

### 📦 Inventory Risk

Several products with fewer than **20 units remaining** have already recorded **40+ historical sales**, indicating immediate replenishment priorities.

---

## 📁 Repository Structure

```text
ecommerce-marketplace-sql/
│
├── 01_schema.sql
├── 02_indexes.sql
├── 03_business_queries.sql
├── load_data.sql
├── generate_data.py
├── benchmark.py
├── benchmark_results.md
│
├── data/
│   ├── customers.csv
│   ├── sellers.csv
│   ├── products.csv
│   ├── orders.csv
│   └── ...
│
└── README.md
```

---

## 🛠️ Technology Stack

### Database
- MySQL / MariaDB

### Data Generation
- Python
- Faker

### Analytics
- Window Functions
- CTEs
- Aggregations

### Performance Engineering
- EXPLAIN Plans
- Composite Indexes
- Query Benchmarking

---

## 🚀 Key Portfolio Highlights

✅ 294,431 synthetic records

✅ Multi-vendor marketplace simulation

✅ Advanced SQL analytics

✅ Window functions & CTEs

✅ Query optimization case study

✅ Documented EXPLAIN analysis

✅ 8.4x dashboard performance improvement

✅ Reproducible benchmark framework

---

## 🎯 Why This Project Matters

This repository goes beyond schema design and demonstrates the complete workflow expected from a modern SQL Developer or Data Analyst:

- Data modeling
- Data generation
- Business analytics
- Performance tuning
- Benchmark-driven optimization
- Documentation and reproducibility

It reflects the type of analytical and engineering work commonly encountered in large-scale e-commerce and marketplace platforms.

---

*All datasets are fully synthetic and generated specifically for this project. No real customer, seller, or transaction data is used.*
