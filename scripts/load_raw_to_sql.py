import os
import pandas as pd
from sqlalchemy import create_engine

RAW_DATA_PATH = "data/raw"
SERVER_NAME = "localhost"
DATABASE_NAME = "OlistDB"

connection_string = f"mssql+pyodbc://@{SERVER_NAME}/{DATABASE_NAME}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes&TrustServerCertificate=yes"

tables = {
    "stg_orders": "olist_orders_dataset.csv",
    "stg_order_items": "olist_order_items_dataset.csv",
    "stg_order_payments": "olist_order_payments_dataset.csv",
    "stg_order_reviews": "olist_order_reviews_dataset.csv",
    "stg_customers": "olist_customers_dataset.csv",
    "stg_sellers": "olist_sellers_dataset.csv",
    "stg_products": "olist_products_dataset.csv",
    "stg_geolocation": "olist_geolocation_dataset.csv",
    "stg_category_translation": "product_category_name_translation.csv"
}

def load_staging_tables():
    """Extract CSVs and load into SQL Server staging area (ELT Load)."""
    engine = create_engine(connection_string)
    for table_name, filename in tables.items():
        file_path = os.path.join(RAW_DATA_PATH, filename)
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df.to_sql(name=table_name, con=engine, if_exists="replace", index=False)
            print(f"Loaded {table_name} ({len(df)} rows)")

if __name__ == "__main__":
    load_staging_tables()