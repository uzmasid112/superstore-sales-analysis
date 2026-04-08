import pandas as pd
from sqlalchemy import create_engine
import urllib.parse
# STEP 1: Load the cleaned CSV file
df = pd.read_csv(r"C:\Uzama\superstore_cleaned.csv")
print(f"Rows to load: {len(df)}")
# STEP 2: SQL Server details
SERVER = r"UZMA-PC\SQLEXPRESS" # Update with your server name
DATABASE = "SalesAnalysisDB"

# STEP 3: Build connection string
params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"Trusted_Connection=yes;"
)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

# STEP 4: Load to SQL Server
df.to_sql(
    name="sales",
    con=engine,
    if_exists="replace",
    index=False
)
print("Data loaded successfully!")
print(f"Table 'sales' created in database '{DATABASE}'")