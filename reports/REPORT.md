<<<<<<< HEAD
BIG DATA ANALYTICS PIPELINE — OLIST E-COMMERCE PROJECT REPORT
Prepared by: Akın Esmeray
Eskişehir Osmangazi University / National Technology Academy - YZ101
Date: July 2026

1. Executive Summary & Architecture Overview
 
This project implements an end-to-end ELT (Extract, Load, Transform) Data Pipeline and Star Schema Data Warehouse architecture built around the Olist Brazilian E-Commerce public dataset (~100,000 real orders from 2016 to 2018). 
The architecture is structured into 4 core layers: 
Data Source Layer: 9 raw CSV datasets extracted from Kaggle. 
ETL / ELT Ingestion Layer: Raw CSVs are ingested directly into SQL Server staging tables (stg_*) using Python (pandas, sqlalchemy) without pre-transformation (Load phase).
Data Warehouse Layer: Raw staging data is cleansed, deduplicated, and transformed into a Star Schema (fact and dim tables) using SQL (Transform phase).
End User / Business Layer: Analytical SQL queries designed to answer core business questions.

2. Data Quality & Deduplication Analysis
Clean Data Definition:
Clean Data refers to reliable, deduplicated, properly type-casted, and structurally standardized datasets prepared for enterprise analytics.
Key Data Issues & Technical Solutions (STUDY Answers):
Is data clean & duplicates?
The olist_geolocation_dataset contains 1,000,163 rows for only 19,015 unique ZIP code prefixes (~52.6x duplicate factor). To prevent row inflation (fan-out) during joins, coordinates were aggregated by calculating average latitude and longitude per ZIP prefix. In order_reviews, multiple review entries per order were deduplicated by retaining only the latest review timestamp.
ETL vs ELT Approach & dbt:
An ELT approach was adopted. Raw data was loaded untouched into SQL Server first, performing all transformations within the data warehouse. dbt acts as the transformation framework orchestrating the pipeline into Staging (Bronze) → Intermediate (Silver) → Marts (Gold) layers with automated data quality testing.
Star Schema & Grain Resolution:
To solve grain mismatches and prevent fan-out, two separate Fact tables were designed:
fact_order_items (Grain: Item level): Dedicated to revenue, category performance, top sellers, and state sales.
fact_orders (Grain: Order level): Dedicated to delivery times, payment method trends, and review scores.






3. Star Schema Mapping Table

 

| Business Question | Fact Table | Dimensions |
|---|---|---|
| Monthly revenue | `fact_order_items` | `dim_date` *(Degenerate Dim in `fact_order_items`)* |
| Revenue by product category | `fact_order_items` | `dim_products` |
| Top-performing sellers | `fact_order_items` | `dim_sellers` |
| Sales by customer state | `fact_order_items` | `dim_customers` |
| Average delivery time by state | `fact_orders` | `dim_customers` |
| Payment method trends | `fact_orders` | N/A *(Degenerate Dim within `fact_orders`)* |
| Average review score by category | `fact_order_items` | `dim_products` *(Joined with `fact_orders` on `order_id`)* |





4. Business Questions & Query Findings
4.1. Monthly Revenue
Tracks monthly historical total revenue and order volume for delivered orders.

[SELECT 
    FORMAT(order_purchase_timestamp, 'yyyy-MM') AS year_month,
    ROUND(SUM(price), 2) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_orders
FROM fact_order_items
WHERE order_status = 'delivered'
GROUP BY FORMAT(order_purchase_timestamp, 'yyyy-MM')
ORDER BY year_month;]

 Key Finding: Peak revenue occurred in November 2017 ($987,765.37 from 7,289 orders).
 
4.2. Revenue by Product Category
Lists the top 10 highest revenue-generating product categories using translated English category names.
[SELECT TOP 10
    p.product_category_name_english,
    ROUND(SUM(f.price), 2) AS total_revenue
FROM fact_order_items f
JOIN dim_products p ON f.product_id = p.product_id
WHERE f.order_status = 'delivered'
GROUP BY p.product_category_name_english
ORDER BY total_revenue DESC;]

Key Finding: Top category is health_beauty with $1,233,131.72 total revenue.
 
4.3. Top-Performing Sellers
Identifies the top 10 sellers by sales volume along with their state locations.

[SELECT TOP 10 
    s.seller_id, 
    s.seller_state, 
    ROUND(SUM(f.price), 2) AS total_sales
FROM fact_order_items f 
JOIN dim_sellers s ON f.seller_id = s.seller_id
WHERE f.order_status = 'delivered' 
GROUP BY s.seller_id, s.seller_state 
ORDER BY total_sales DESC;]

Key Finding: Top seller 4869f7a5dfa277a7dca6462dcf3b52b2 in SP state generated $226,987.93 across 1,124 orders.

 
4.4. Sales by Customer State
Breaks down revenue and total orders across customer states.

[SELECT 
    c.customer_state, 
    COUNT(DISTINCT f.order_id) AS total_orders, 
    ROUND(SUM(f.price), 2) AS total_sales
FROM fact_order_items f 
JOIN dim_customers c ON f.customer_id = c.customer_id
WHERE f.order_status = 'delivered' 
GROUP BY c.customer_state 
ORDER BY total_sales DESC;]

Key Finding: São Paulo (SP) dominates overall market sales with $5,067,633.16 total
 
4.5. Average Delivery Time by State
Calculates average order delivery duration (in days) grouped by customer state.

[SELECT 
    c.customer_state, 
    ROUND(AVG(CAST(o.delivery_time_days AS FLOAT)), 1) AS avg_delivery_days
FROM fact_orders o 
JOIN dim_customers c ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered' 
GROUP BY c.customer_state 
ORDER BY avg_delivery_days ASC;]

Key Finding: SP achieved the fastest delivery average (8.7 days), while remote states like RR averaged 29.3 days
 

4.6. Payment Method Trends
Analyzes transaction volume and total monetary value across top payment method combinations.

[SELECT 
    payment_methods,
    COUNT(order_id) AS total_transactions,
    ROUND(SUM(total_payment_value), 2) AS total_paid_amount
FROM fact_orders
WHERE payment_methods IS NOT NULL
GROUP BY payment_methods
ORDER BY total_transactions DESC;]

Key Finding: Credit card is the primary payment choice with 73,972 orders ($12.29M total paid), followed by Boleto.
 
4.7. Average Review Score by Category
Ranks product categories with at least 100 orders by their average customer review score.

[SELECT TOP 10 
    p.product_category_name_english, 
    ROUND(AVG(CAST(o.review_score AS FLOAT)), 2) AS avg_review_score
FROM fact_order_items i 
JOIN dim_products p ON i.product_id = p.product_id 
JOIN fact_orders o ON i.order_id = o.order_id
WHERE o.review_score IS NOT NULL 
GROUP BY p.product_category_name_english 
HAVING COUNT(DISTINCT o.order_id) >= 100 
ORDER BY avg_review_score DESC;]


Key Finding: books_general_interest scored the highest customer satisfaction with an average rating of 4.45 / 5.00.
 
5. Conclusion
The pipeline successfully converts raw e-commerce records into a clean, query-optimized Data Warehouse, ensuring strict data integrity across all analytical business metrics.

=======
### Report 
Write your report here. Include any relevant data, analysis, and conclusions. Make sure to structure your report with clear headings and subheadings for easy navigation.
>>>>>>> upstream/master
