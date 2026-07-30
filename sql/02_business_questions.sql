-- ===================================================================
-- Project: Olist E-Commerce Business Intelligence Queries
-- Description: Analytical SQL Queries solving core business questions
-- ===================================================================

USE OlistDB;
GO

-- 1. Monthly Revenue
SELECT 
    FORMAT(order_purchase_timestamp, 'yyyy-MM') AS year_month,
    ROUND(SUM(price), 2) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_orders
FROM fact_order_items
WHERE order_status = 'delivered'
GROUP BY FORMAT(order_purchase_timestamp, 'yyyy-MM')
ORDER BY year_month;

-- 2. Revenue by Product Category
SELECT TOP 10
    p.product_category_name_english,
    ROUND(SUM(f.price), 2) AS total_revenue,
    COUNT(f.order_id) AS items_sold
FROM fact_order_items f
JOIN dim_products p ON f.product_id = p.product_id
WHERE f.order_status = 'delivered'
GROUP BY p.product_category_name_english
ORDER BY total_revenue DESC;

-- 3. Top-Performing Sellers
SELECT TOP 10
    s.seller_id,
    s.seller_state,
    ROUND(SUM(f.price), 2) AS total_sales,
    COUNT(DISTINCT f.order_id) AS total_orders
FROM fact_order_items f
JOIN dim_sellers s ON f.seller_id = s.seller_id
WHERE f.order_status = 'delivered'
GROUP BY s.seller_id, s.seller_state
ORDER BY total_sales DESC;

-- 4. Sales by Customer State
SELECT 
    c.customer_state,
    COUNT(DISTINCT f.order_id) AS total_orders,
    ROUND(SUM(f.price), 2) AS total_sales
FROM fact_order_items f
JOIN dim_customers c ON f.customer_id = c.customer_id
WHERE f.order_status = 'delivered'
GROUP BY c.customer_state
ORDER BY total_sales DESC;

-- 5. Average Delivery Time by State
SELECT 
    c.customer_state,
    ROUND(AVG(CAST(o.delivery_time_days AS FLOAT)), 1) AS avg_delivery_days,
    COUNT(o.order_id) AS total_delivered_orders
FROM fact_orders o
JOIN dim_customers c ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered' AND o.delivery_time_days IS NOT NULL
GROUP BY c.customer_state
ORDER BY avg_delivery_days ASC;

-- 6. Payment Method Trends
SELECT 
    payment_methods,
    COUNT(order_id) AS total_transactions,
    ROUND(SUM(total_payment_value), 2) AS total_paid_amount
FROM fact_orders
WHERE payment_methods IS NOT NULL
GROUP BY payment_methods
ORDER BY total_transactions DESC;

-- 7. Average Review Score by Category
SELECT TOP 10
    p.product_category_name_english,
    ROUND(AVG(CAST(o.review_score AS FLOAT)), 2) AS avg_review_score,
    COUNT(DISTINCT o.order_id) AS total_reviews
FROM fact_order_items i
JOIN dim_products p ON i.product_id = p.product_id
JOIN fact_orders o ON i.order_id = o.order_id
WHERE o.review_score IS NOT NULL
GROUP BY p.product_category_name_english
HAVING COUNT(DISTINCT o.order_id) >= 100
ORDER BY avg_review_score DESC;