"""
Step 1: Clean the raw Superstore sales data.

Reads  data/superstore_sales.csv
Writes outputs/superstore_cleaned.csv

Run from the repository root:  python python/01_cleaning.py
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW_FILE = ROOT / "data" / "superstore_sales.csv"
CLEAN_FILE = ROOT / "outputs" / "superstore_cleaned.csv"

# ── STEP 1: Load the CSV file ──────────────────────────────────────────
df = pd.read_csv(RAW_FILE, encoding="latin-1")
print("Data loaded:", df.shape)  # rows, columns

# ── STEP 2: First look at the data ─────────────────────────────────────
print("\nFirst 5 rows:")
print(df.head())
print("\nMissing values per column:")
print(df.isnull().sum())

# ── STEP 3: Clean column names ─────────────────────────────────────────
# Lowercase with underscores, so the names work in SQL without quotes
df.columns = (
    df.columns.str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
)
print("\nCleaned columns:", df.columns.tolist())

# ── STEP 4: Fix data types ─────────────────────────────────────────────
# Dates are stored as text in DD/MM/YYYY format
df["order_date"] = pd.to_datetime(df["order_date"], format="%d/%m/%Y")
df["ship_date"] = pd.to_datetime(df["ship_date"], format="%d/%m/%Y")

# ── STEP 5: Data quality checks ────────────────────────────────────────
before = len(df)
df = df.dropna(subset=["sales", "order_id"])  # rows we cannot analyze
print(f"\nRows dropped for missing sales or order ID: {before - len(df)}")
print(f"Duplicate rows: {df.duplicated().sum()}")
print(f"Orders shipped before they were placed: {(df['ship_date'] < df['order_date']).sum()}")

# 11 rows have no postal code (all for Burlington, Vermont). Postal code is
# not used in the analysis, so these rows are kept.

# ── STEP 6: Add a useful column ────────────────────────────────────────
# Days between order and shipping, for delivery analysis
df["days_to_ship"] = (df["ship_date"] - df["order_date"]).dt.days

# ── STEP 7: Save the cleaned file ──────────────────────────────────────
CLEAN_FILE.parent.mkdir(exist_ok=True)
df.to_csv(CLEAN_FILE, index=False)
print(f"\nCleaned data {df.shape} saved to {CLEAN_FILE.relative_to(ROOT)}")
