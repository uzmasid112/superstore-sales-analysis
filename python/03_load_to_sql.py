"""
Step 3: Load the cleaned data into SQL Server.

Reads  outputs/superstore_cleaned.csv
Writes table dbo.sales in the SalesAnalysisDB database

Before running, set SERVER to your own SQL Server instance name
(shown in the SSMS "Connect to Server" window).

Run from the repository root:  python python/03_load_to_sql.py
"""
from pathlib import Path
import urllib.parse

import pandas as pd
from sqlalchemy import create_engine

ROOT = Path(__file__).resolve().parent.parent
CLEAN_FILE = ROOT / "outputs" / "superstore_cleaned.csv"

SERVER = r"YOUR_SERVER_NAME\SQLEXPRESS"   # update this
DATABASE = "SalesAnalysisDB"

# STEP 1: Load the cleaned CSV
df = pd.read_csv(CLEAN_FILE, parse_dates=["order_date", "ship_date"])
print(f"Rows to load: {len(df):,}")

# STEP 2: Build the connection (Windows authentication)
params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    "Trusted_Connection=yes;"
)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

# STEP 3: Write the table (replaces it if it already exists)
df.to_sql(name="sales", con=engine, if_exists="replace", index=False)
print(f"Table 'sales' created in database '{DATABASE}'")
