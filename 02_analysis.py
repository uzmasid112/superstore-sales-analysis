import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the cleaned data
df = pd.read_csv("superstore_cleaned.csv")

print("=== SUPERSTORE SALES ANALYSIS ===")
print(f"Dataset shape: {df.shape}")
print(f"Date range: {df['order_date'].min()} to {df['order_date'].max()}")

# Basic statistics
print("\n=== SALES STATISTICS ===")
print(f"Total Sales: ${df['sales'].sum():,.2f}")
print(f"Average Order Value: ${df['sales'].mean():.2f}")
print(f"Median Order Value: ${df['sales'].median():.2f}")
print(f"Maximum Order Value: ${df['sales'].max():.2f}")
print(f"Minimum Order Value: ${df['sales'].min():.2f}")

# Sales by Category
print("\n=== SALES BY CATEGORY ===")
category_sales = df.groupby('category')['sales'].sum().sort_values(ascending=False)
for category, sales in category_sales.items():
    print(f"{category}: ${sales:,.2f}")

# Sales by Region
print("\n=== SALES BY REGION ===")
region_sales = df.groupby('region')['sales'].sum().sort_values(ascending=False)
for region, sales in region_sales.items():
    print(f"{region}: ${sales:,.2f}")

# Top 10 Customers by Sales
print("\n=== TOP 10 CUSTOMERS BY SALES ===")
top_customers = df.groupby('customer_name')['sales'].sum().sort_values(ascending=False).head(10)
for i, (customer, sales) in enumerate(top_customers.items(), 1):
    print(f"{i}. {customer}: ${sales:,.2f}")

# Monthly Sales Trend
df['order_date'] = pd.to_datetime(df['order_date'])
df['month_year'] = df['order_date'].dt.to_period('M')
monthly_sales = df.groupby('month_year')['sales'].sum()

print("\n=== MONTHLY SALES TREND (First 12 months) ===")
for period, sales in monthly_sales.head(12).items():
    print(f"{period}: ${sales:,.2f}")

# Create visualizations
plt.figure(figsize=(15, 10))

# Sales by Category
plt.subplot(2, 2, 1)
category_sales.plot(kind='bar', color='skyblue')
plt.title('Sales by Category')
plt.ylabel('Sales ($)')
plt.xticks(rotation=45)

# Sales by Region
plt.subplot(2, 2, 2)
region_sales.plot(kind='bar', color='lightgreen')
plt.title('Sales by Region')
plt.ylabel('Sales ($)')
plt.xticks(rotation=45)

# Monthly Sales Trend
plt.subplot(2, 2, 3)
monthly_sales.plot(kind='line', marker='o', color='orange')
plt.title('Monthly Sales Trend')
plt.ylabel('Sales ($)')
plt.xticks(rotation=45)

# Sales Distribution
plt.subplot(2, 2, 4)
plt.hist(df['sales'], bins=50, color='purple', alpha=0.7)
plt.title('Sales Distribution')
plt.xlabel('Sales Amount ($)')
plt.ylabel('Frequency')

plt.tight_layout()
plt.savefig('sales_analysis.png', dpi=300, bbox_inches='tight')
print("\n=== VISUALIZATIONS SAVED ===")
print("Chart saved as 'sales_analysis.png'")

# Save summary to CSV
summary = pd.DataFrame({
    'Metric': ['Total Sales', 'Average Order', 'Total Orders', 'Unique Customers', 'Unique Products'],
    'Value': [
        df['sales'].sum(),
        df['sales'].mean(),
        len(df),
        df['customer_id'].nunique(),
        df['product_id'].nunique()
    ]
})
summary.to_csv('sales_summary.csv', index=False)
print("Summary saved as 'sales_summary.csv'")

print("\n=== ANALYSIS COMPLETE ===")
print("Your cleaned Superstore data has been analyzed!")
print("Check the generated files: sales_analysis.png and sales_summary.csv")