<<<<<<< HEAD
import os
import pandas as pd
import duckdb

RAW_DATA_PATH = "data/raw"
PARQUET_DATA_PATH = "data/parquet"

csv_files = {
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "products": "olist_products_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "category_translation": "product_category_name_translation.csv"
}

def load_data():
    """Load raw CSV datasets into DataFrames for analysis."""
    dfs = {}
    for key, filename in csv_files.items():
        path = os.path.join(RAW_DATA_PATH, filename)
        if os.path.exists(path):
            dfs[key] = pd.read_csv(path)
    return dfs

def analyze_data_quality():
    """Perform comprehensive data quality analysis (Duplicates & Distributions)."""
    dfs = load_data()
    if not dfs:
        print("Data files not found.")
        return

    print("--- 1. GEOLOCATION DUPLICATE ANALYSIS ---")
    geo_df = dfs["geolocation"]
    total_geo = len(geo_df)
    unique_zip = geo_df["geolocation_zip_code_prefix"].nunique()
    print(f"Total Geolocation Rows : {total_geo:,}")
    print(f"Unique Zip Code Prefixes : {unique_zip:,}")
    print(f"Duplicate Ratio        : {total_geo / unique_zip:.2f}x average per zip prefix\n")

    print("--- 2. REVIEWS DUPLICATE ANALYSIS ---")
    rev_df = dfs["order_reviews"]
    print(f"Total Review Rows      : {len(rev_df):,}")
    print(f"Unique Review IDs      : {rev_df['review_id'].nunique():,}")
    print(f"Unique Order IDs       : {rev_df['order_id'].nunique():,}\n")

    print("--- 3. CUSTOMER KEY ANALYSIS ---")
    cust_df = dfs["customers"]
    print(f"Total customer_id (Order Transient) : {cust_df['customer_id'].nunique():,}")
    print(f"Unique customer_unique_id (True ID) : {cust_df['customer_unique_id'].nunique():,}\n")

    print("--- 4. ORDER STATUS DISTRIBUTION ---")
    ord_df = dfs["orders"]
    print(ord_df["order_status"].value_counts().to_string())
    print("\n" + "="*50 + "\n")

def convert_to_parquet():
    """Convert raw CSV datasets to Parquet format using DuckDB."""
    print("--- CONVERTING CSV TO PARQUET ---")
    for table_name, filename in csv_files.items():
        csv_path = os.path.join(RAW_DATA_PATH, filename).replace("\\", "/")
        parquet_dir = os.path.join(PARQUET_DATA_PATH, table_name).replace("\\", "/")
        parquet_file = f"{parquet_dir}/{table_name}.parquet"
        
        if os.path.exists(csv_path):
            os.makedirs(parquet_dir, exist_ok=True)
            duckdb.query(f"COPY (SELECT * FROM read_csv_auto('{csv_path}')) TO '{parquet_file}' (FORMAT PARQUET, COMPRESSION SNAPPY)")
            print(f"Converted: {table_name}")

if __name__ == "__main__":
    analyze_data_quality()
    convert_to_parquet()
=======
if __name__ == "__main__":
    print("Implement your code here")
>>>>>>> upstream/master
