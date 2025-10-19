# Db Load Testing file to verify data load into the database
import pandas as pd
import sqlite3
from pathlib import Path

# Build absolute path to the database file
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / 'database' / 'a2_pipeline.db'

def test_products_table_exists():
    # Assert that the database file exists
    assert DB_PATH.exists(), f"Database file does not exist at {DB_PATH}"
    # Connect to the SQLite database
    db_connection = sqlite3.connect(DB_PATH)
    cursor = db_connection.cursor()
    
    # Check if the 'products' table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall()]
    assert 'products' in tables, "Table 'products' does not exist in the database."
    
    db_connection.close()

def test_products_data_preview():
    # Connect to the SQLite database
    db_connection = sqlite3.connect(DB_PATH)
    
    # Load data from the 'products' table
    df = pd.read_sql_query("SELECT * FROM products LIMIT 5;", db_connection)
    
    db_connection.close()
    
    # Check if the dataframe is not empty
    assert not df.empty, "No data found in 'products' table."
    