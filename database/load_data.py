## Load Data file to populate the database from raw_products.csv
import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

# --- 1. Define file paths ---`
data_dir = Path(__file__).resolve().parent.parent / "data"
raw_data_file = data_dir / "raw_products.csv"

# --- 2. Load raw CSV data ---
raw_csv_data = pd.read_csv(raw_data_file)

# preview the raw data
print("Raw CSV preview:")   
print(raw_csv_data.head())

# --- 3. Basic Data Cleaning ---
raw_csv_data.columns = [c.strip().lower() for c in raw_csv_data.columns] # normalize clean column names
raw_csv_data['category'] = raw_csv_data['category'].str.strip().str.title() # title case
raw_csv_data['product_name'] = raw_csv_data['product_name'].str.strip() # strip whitespace from product names

# Fill in missing values
raw_csv_data['features'] = raw_csv_data['features'].fillna("No description provided.")
raw_csv_data['rating'] = raw_csv_data['rating'].fillna(0)

# print clean data 
print("\nCleaned data preview:")
print(raw_csv_data.head())

# --- 4. Create SQLite database connection ---
engine = create_engine('sqlite:///database/a2_pipeline.db')

# --- 5. Load cleaned data into SQL database ---   
table_name = 'products'
raw_csv_data.to_sql(table_name, con=engine, if_exists='replace', index=False)

# Print success message
print(f"\n✅ Data successfully loaded into SQLite table '{table_name}' in 'a2_pipeline.db' database.")
print("Database file created: a2_pipeline.db")
