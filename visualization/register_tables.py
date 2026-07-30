<<<<<<< HEAD
import os
from sqlalchemy import create_engine

# Database credentials
SERVER_NAME = "localhost"
DATABASE_NAME = "OlistDB"

connection_string = f"mssql+pyodbc://@{SERVER_NAME}/{DATABASE_NAME}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes&TrustServerCertificate=yes"

def register_dw_tables():
    """Validate data warehouse connections for analytical dashboards."""
    try:
        engine = create_engine(connection_string)
        with engine.connect() as conn:
            print("Database connection successfully verified.")
    except Exception as err:
        print(f"Connection failed: {err}")

if __name__ == "__main__":
    register_dw_tables()
=======
"""
You may probably need to register your tables in order to visualize them.
Do it here in this file
"""

if __name__ == "__main__":
    print("Registering tables...")
>>>>>>> upstream/master
