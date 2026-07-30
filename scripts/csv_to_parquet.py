import os
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

def convert_to_parquet():
    """Convert raw CSV files to Snappy-compressed Parquet files using DuckDB."""
    print("--- STARTING CSV TO PARQUET CONVERSION ---")
    for table_name, filename in csv_files.items():
        csv_path = os.path.join(RAW_DATA_PATH, filename).replace("\\", "/")
        parquet_dir = os.path.join(PARQUET_DATA_PATH, table_name).replace("\\", "/")
        parquet_file = f"{parquet_dir}/{table_name}.parquet"
        
        if os.path.exists(csv_path):
            os.makedirs(parquet_dir, exist_ok=True)
            duckdb.query(f"COPY (SELECT * FROM read_csv_auto('{csv_path}')) TO '{parquet_file}' (FORMAT PARQUET, COMPRESSION SNAPPY)")
            print(f"Converted: {table_name} -> {parquet_file}")
        else:
            print(f"File missing: {csv_path}")

if __name__ == "__main__":
    convert_to_parquet()