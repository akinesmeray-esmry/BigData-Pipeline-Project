-- ===================================================================
-- Project: Olist E-Commerce Data Warehouse (Star Schema)
-- Description: Creates Fact and Dimension tables from Staging Layer
-- ===================================================================

USE OlistDB;
GO

-------------------------------------------------------------------
-- 1. Dimension: Customers (dim_customers)
-------------------------------------------------------------------
IF OBJECT_ID('dim_customers', 'U') IS NOT NULL DROP TABLE dim_customers;

SELECT 
    customer_id,
    customer_unique_id,
    customer_zip_code_prefix,
    customer_city,
    customer_state
INTO dim_customers
FROM stg_customers;

-------------------------------------------------------------------
-- 2. Dimension: Products (dim_products)
-------------------------------------------------------------------
IF OBJECT_ID('dim_products', 'U') IS NOT NULL DROP TABLE dim_products;

SELECT 
    p.product_id,
    p.product_category_name,
    COALESCE(t.product_category_name_english, p.product_category_name, 'unknown') AS product_category_name_english,
    p.product_weight_g,
    p.product_length_cm,
    p.product_height_cm,
    p.product_width_cm
INTO dim_products
FROM stg_products p
LEFT JOIN stg_category_translation t 
    ON p.product_category_name = t.product_category_name;

-------------------------------------------------------------------
-- 3. Dimension: Sellers (dim_sellers)
-------------------------------------------------------------------
IF OBJECT_ID('dim_sellers', 'U') IS NOT NULL DROP TABLE dim_sellers;

SELECT 
    seller_id,
    seller_zip_code_prefix,
    seller_city,
    seller_state
INTO dim_sellers
FROM stg_sellers;

-------------------------------------------------------------------
-- 4. Fact: Order Items (fact_order_items - Grain: Item Level)
-------------------------------------------------------------------
IF OBJECT_ID('fact_order_items', 'U') IS NOT NULL DROP TABLE fact_order_items;

SELECT 
    i.order_id,
    i.order_item_id,
    i.product_id,
    i.seller_id,
    o.customer_id,
    o.order_status,
    CAST(o.order_purchase_timestamp AS DATETIME) AS order_purchase_timestamp,
    i.price,
    i.freight_value,
    ROUND((i.price + i.freight_value), 2) AS total_item_cost
INTO fact_order_items
FROM stg_order_items i
JOIN stg_orders o ON i.order_id = o.order_id;

-------------------------------------------------------------------
-- 5. Fact: Orders (fact_orders - Grain: Order Level)
-------------------------------------------------------------------
IF OBJECT_ID('fact_orders', 'U') IS NOT NULL DROP TABLE fact_orders;

WITH LatestReviews AS (
    SELECT 
        order_id,
        review_score,
        ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY review_creation_date DESC) AS rn
    FROM stg_order_reviews
),
AggregatedPayments AS (
    SELECT 
        order_id,
        STRING_AGG(payment_type, '_') WITHIN GROUP (ORDER BY payment_type) AS payment_methods,
        SUM(payment_value) AS total_payment_value,
        MAX(payment_installments) AS max_installments
    FROM stg_order_payments
    GROUP BY order_id
)
SELECT 
    o.order_id,
    o.customer_id,
    o.order_status,
    CAST(o.order_purchase_timestamp AS DATETIME) AS order_purchase_timestamp,
    CAST(o.order_delivered_customer_date AS DATETIME) AS order_delivered_customer_date,
    CAST(o.order_estimated_delivery_date AS DATETIME) AS order_estimated_delivery_date,
    DATEDIFF(day, CAST(o.order_purchase_timestamp AS DATETIME), CAST(o.order_delivered_customer_date AS DATETIME)) AS delivery_time_days,
    r.review_score,
    p.payment_methods,
    p.total_payment_value,
    p.max_installments
INTO fact_orders
FROM stg_orders o
LEFT JOIN LatestReviews r ON o.order_id = r.order_id AND r.rn = 1
LEFT JOIN AggregatedPayments p ON o.order_id = p.order_id;