-- =========================================================
-- E-Commerce Multi-Seller Marketplace — Schema
-- =========================================================

CREATE DATABASE IF NOT EXISTS marketplace_db;
USE marketplace_db;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS commissions;
DROP TABLE IF EXISTS returns;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS sellers;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS categories;

-- ---------------------------------------------------------
CREATE TABLE customers (
    customer_id     INT PRIMARY KEY AUTO_INCREMENT,
    full_name       VARCHAR(100) NOT NULL,
    email           VARCHAR(150) NOT NULL UNIQUE,
    city            VARCHAR(80),
    country         VARCHAR(80),
    signup_date     DATE NOT NULL
);

-- ---------------------------------------------------------
CREATE TABLE sellers (
    seller_id       INT PRIMARY KEY AUTO_INCREMENT,
    business_name   VARCHAR(120) NOT NULL,
    email           VARCHAR(150) NOT NULL UNIQUE,
    city            VARCHAR(80),
    country         VARCHAR(80),
    joined_date     DATE NOT NULL,
    rating          DECIMAL(3,2) DEFAULT 0.00
);

-- ---------------------------------------------------------
CREATE TABLE categories (
    category_id     INT PRIMARY KEY AUTO_INCREMENT,
    category_name   VARCHAR(80) NOT NULL UNIQUE
);

-- ---------------------------------------------------------
CREATE TABLE products (
    product_id      INT PRIMARY KEY AUTO_INCREMENT,
    seller_id       INT NOT NULL,
    category_id     INT NOT NULL,
    product_name    VARCHAR(150) NOT NULL,
    price           DECIMAL(10,2) NOT NULL,
    stock_quantity  INT NOT NULL DEFAULT 0,
    created_at      DATE NOT NULL,
    FOREIGN KEY (seller_id) REFERENCES sellers(seller_id),
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

-- ---------------------------------------------------------
CREATE TABLE orders (
    order_id        INT PRIMARY KEY AUTO_INCREMENT,
    customer_id     INT NOT NULL,
    order_date      DATETIME NOT NULL,
    order_status    ENUM('placed','shipped','delivered','cancelled','returned') NOT NULL DEFAULT 'placed',
    payment_method  ENUM('card','upi','netbanking','cod','wallet') NOT NULL,
    total_amount    DECIMAL(12,2) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- ---------------------------------------------------------
CREATE TABLE order_items (
    order_item_id   INT PRIMARY KEY AUTO_INCREMENT,
    order_id        INT NOT NULL,
    product_id      INT NOT NULL,
    seller_id       INT NOT NULL,
    quantity        INT NOT NULL,
    unit_price      DECIMAL(10,2) NOT NULL,
    line_total      DECIMAL(12,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
);

-- ---------------------------------------------------------
CREATE TABLE reviews (
    review_id       INT PRIMARY KEY AUTO_INCREMENT,
    product_id      INT NOT NULL,
    customer_id     INT NOT NULL,
    rating          TINYINT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    review_text      VARCHAR(500),
    review_date     DATE NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- ---------------------------------------------------------
CREATE TABLE returns (
    return_id       INT PRIMARY KEY AUTO_INCREMENT,
    order_item_id   INT NOT NULL,
    return_reason   VARCHAR(200),
    return_date     DATE NOT NULL,
    refund_amount   DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_item_id) REFERENCES order_items(order_item_id)
);

-- ---------------------------------------------------------
CREATE TABLE commissions (
    commission_id   INT PRIMARY KEY AUTO_INCREMENT,
    order_item_id   INT NOT NULL,
    seller_id       INT NOT NULL,
    commission_rate DECIMAL(5,2) NOT NULL,
    commission_amount DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_item_id) REFERENCES order_items(order_item_id),
    FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
);

SET FOREIGN_KEY_CHECKS = 1;
