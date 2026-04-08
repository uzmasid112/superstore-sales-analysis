import pandas as pd
# ── STEP 1: Load the CSV file into Python ──────────────────────────────
# pd.read_csv reads the file and turns it into a "DataFrame" (like an Excel table in Python)
try:
    df = pd.read_csv("superstore.csv.csv", encoding="latin-1")  # Use the correct encoding for your file
    print("Data loaded successfully!")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")

    # ── STEP 2: First look at the data ─────────────────────────────────────
    print("Shape:", df.shape)          # how many rows and columns?
    print("\nFirst 5 rows:")
    print(df.head())                   # show the first 5 rows
    print("\nColumn names:")
    print(df.columns.tolist())         # list all column names
    print("\nMissing values:")
    print(df.isnull().sum())           # count missing values in each column

    # ── STEP 3: Clean column names ─────────────────────────────────────────
    # Remove spaces and make everything lowercase so SQL doesn't complain
    df.columns = df.columns.str.lower().str.replace(" ", "_").str.replace("-", "_")
    print("\nCleaned columns:", df.columns.tolist())

    # ── STEP 4: Fix data types ─────────────────────────────────────────────
    # Dates should be date type, not text
    # Note: Dates are in DD/MM/YYYY format, so we specify dayfirst=True
    df["order_date"] = pd.to_datetime(df["order_date"], dayfirst=True)
    df["ship_date"]  = pd.to_datetime(df["ship_date"], dayfirst=True)

    # ── STEP 5: Drop rows where the most important columns are missing ──────
    # Note: This dataset doesn't have a 'profit' column, only 'sales'
    df.dropna(subset=["sales", "order_id"], inplace=True)

    # ── STEP 6: Add a useful new column ────────────────────────────────────
    # Since there's no profit column, we'll skip profit margin calculation
    # You could add other calculated columns here if needed

    # ── STEP 7: Final check ────────────────────────────────────────────────
    print("\nCleaned data shape:", df.shape)
    print(df.dtypes)   # shows the data type of each column

    # Save the cleaned file so we can use it again
    df.to_csv("superstore_cleaned.csv", index=False)
    print("\nCleaned file saved!")

except Exception as e:
    print(f"Error: {e}")