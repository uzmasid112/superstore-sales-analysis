"""
Step 2: Analyze the cleaned Superstore sales data.

Reads  outputs/superstore_cleaned.csv   (created by 01_cleaning.py)
Writes outputs/sales_summary.csv and images/sales_analysis.png

Run from the repository root:  python python/02_analysis.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
CLEAN_FILE = ROOT / "outputs" / "superstore_cleaned.csv"
SUMMARY_FILE = ROOT / "outputs" / "sales_summary.csv"
CHART_FILE = ROOT / "images" / "sales_analysis.png"

df = pd.read_csv(CLEAN_FILE, parse_dates=["order_date", "ship_date"])

print("=== SUPERSTORE SALES ANALYSIS ===")
print(f"Dataset shape: {df.shape}")
print(f"Date range: {df['order_date'].min():%Y-%m-%d} to {df['order_date'].max():%Y-%m-%d}")

# ── Headline numbers ───────────────────────────────────────────────────
total_sales = df["sales"].sum()
total_orders = df["order_id"].nunique()   # one order can have many lines
avg_order_value = total_sales / total_orders

print("\n=== SALES STATISTICS ===")
print(f"Total sales:          ${total_sales:,.2f}")
print(f"Orders:               {total_orders:,}  ({len(df):,} order lines)")
print(f"Average order value:  ${avg_order_value:,.2f}")
print(f"Average line value:   ${df['sales'].mean():,.2f}")
print(f"Median line value:    ${df['sales'].median():,.2f}")

# ── Sales by category, region and segment ──────────────────────────────
category_sales = df.groupby("category")["sales"].sum().sort_values(ascending=False)
region_sales = df.groupby("region")["sales"].sum().sort_values(ascending=False)
segment_sales = df.groupby("segment")["sales"].sum().sort_values(ascending=False)

for title, series in [("CATEGORY", category_sales), ("REGION", region_sales), ("SEGMENT", segment_sales)]:
    print(f"\n=== SALES BY {title} ===")
    for name, sales in series.items():
        print(f"{name:<16} ${sales:>12,.2f}  ({sales / total_sales:.1%})")

# ── Top 10 customers ───────────────────────────────────────────────────
print("\n=== TOP 10 CUSTOMERS BY SALES ===")
top_customers = df.groupby("customer_name")["sales"].sum().sort_values(ascending=False).head(10)
for i, (customer, sales) in enumerate(top_customers.items(), 1):
    print(f"{i:>2}. {customer:<22} ${sales:,.2f}")

# ── Yearly growth and monthly trend ────────────────────────────────────
yearly_sales = df.groupby(df["order_date"].dt.year)["sales"].sum()
yearly_growth = yearly_sales.pct_change()
print("\n=== SALES BY YEAR ===")
for year, sales in yearly_sales.items():
    growth = yearly_growth[year]
    note = "" if pd.isna(growth) else f"  ({growth:+.1%} vs prior year)"
    print(f"{year}: ${sales:,.2f}{note}")

monthly_sales = df.groupby(df["order_date"].dt.to_period("M"))["sales"].sum()

# ── Charts ─────────────────────────────────────────────────────────────
plt.figure(figsize=(15, 10))

plt.subplot(2, 2, 1)
category_sales.plot(kind="bar", color="skyblue")
plt.title("Sales by Category")
plt.ylabel("Sales ($)")
plt.xlabel("")
plt.xticks(rotation=0)

plt.subplot(2, 2, 2)
region_sales.plot(kind="bar", color="lightgreen")
plt.title("Sales by Region")
plt.ylabel("Sales ($)")
plt.xlabel("")
plt.xticks(rotation=0)

plt.subplot(2, 2, 3)
monthly_sales.plot(kind="line", marker="o", color="orange")
plt.title("Monthly Sales Trend")
plt.ylabel("Sales ($)")
plt.xlabel("")

plt.subplot(2, 2, 4)
plt.hist(df["sales"], bins=50, color="purple", alpha=0.7)
plt.title("Order Line Value Distribution")
plt.xlabel("Sales per line ($)")
plt.ylabel("Number of order lines")

plt.tight_layout()
CHART_FILE.parent.mkdir(exist_ok=True)
plt.savefig(CHART_FILE, dpi=150, bbox_inches="tight")
print(f"\nChart saved to {CHART_FILE.relative_to(ROOT)}")

# ── Summary table ──────────────────────────────────────────────────────
summary = pd.DataFrame({
    "metric": ["Total sales", "Orders", "Order lines", "Average order value",
               "Unique customers", "Unique products"],
    "value": [round(total_sales, 2), total_orders, len(df), round(avg_order_value, 2),
              df["customer_id"].nunique(), df["product_id"].nunique()],
})
summary.to_csv(SUMMARY_FILE, index=False)
print(f"Summary saved to {SUMMARY_FILE.relative_to(ROOT)}")
