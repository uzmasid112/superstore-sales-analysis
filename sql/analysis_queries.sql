/* =====================================================================
   Superstore Sales Analysis (SQL Server / T-SQL)
   Author:  Uzma Siddiqui
   Table:   dbo.sales, loaded from outputs/superstore_cleaned.csv by
            python/03_load_to_sql.py (9,800 order lines, 2015-2018)

   Queries
     1. Headline numbers: revenue, orders, order lines
     2. Revenue by region
     3. Top 10 products
     4. Monthly sales trend
     5. Sales by category and sub-category
     6. Bottom 10 products
   ===================================================================== */

USE SalesAnalysisDB;
GO


-- ── QUERY 1: Headline numbers ─────────────────────────────────────────
-- One order can contain several products, so orders are counted with
-- COUNT(DISTINCT order_id) and order lines with COUNT(*).
SELECT
    COUNT(DISTINCT order_id)                                  AS total_orders,
    ROUND(SUM(sales), 2)                                      AS total_revenue,
    COUNT(*)                                                  AS total_lines,
    ROUND(AVG(sales), 2)                                      AS avg_sale_per_line,
    ROUND(SUM(sales) / COUNT(DISTINCT order_id), 2)           AS avg_order_value
FROM dbo.sales;

-- Finding: 4,922 orders, 2.26M in revenue, average order value about 459.


-- ── QUERY 2: Revenue by region ────────────────────────────────────────
SELECT
    region,
    ROUND(SUM(sales), 2)        AS total_sales,
    COUNT(*)                    AS line_count,
    COUNT(DISTINCT order_id)    AS order_count
FROM dbo.sales
GROUP BY region
ORDER BY total_sales DESC;

-- Finding: West (31%) and East (30%) bring in over 60% of revenue;
-- South is the smallest region at 17%.


-- ── QUERY 3: Top 10 best-selling products ─────────────────────────────
SELECT TOP 10
    product_name,
    ROUND(SUM(sales), 2)        AS total_sales,
    COUNT(*)                    AS times_sold,
    COUNT(DISTINCT order_id)    AS order_count
FROM dbo.sales
GROUP BY product_name
ORDER BY total_sales DESC;

-- Finding: the Canon imageCLASS 2200 Advanced Copier leads with about
-- 61,600 in sales, more than twice the next product.


-- ── QUERY 4: Monthly sales trend ──────────────────────────────────────
SELECT
    FORMAT(CAST(order_date AS datetime), 'yyyy-MM')   AS month,
    ROUND(SUM(sales), 2)                              AS monthly_sales,
    COUNT(DISTINCT order_id)                          AS monthly_orders
FROM dbo.sales
GROUP BY FORMAT(CAST(order_date AS datetime), 'yyyy-MM')
ORDER BY month;

-- Finding: sales peak every year in September, November and December,
-- which together bring in 43% of annual revenue.


-- ── QUERY 5: Sales by category and sub-category ───────────────────────
SELECT
    category,
    sub_category,
    ROUND(SUM(sales), 2)        AS total_sales,
    COUNT(*)                    AS line_count,
    COUNT(DISTINCT order_id)    AS order_count
FROM dbo.sales
GROUP BY category, sub_category
ORDER BY category, total_sales DESC;

-- Finding: Technology is the largest category (37%). Phones and Chairs
-- are the top two sub-categories, at about 328K and 323K.


-- ── QUERY 6: Bottom 10 lowest-selling products ────────────────────────
SELECT TOP 10
    product_name,
    ROUND(SUM(sales), 2)        AS total_sales,
    COUNT(*)                    AS times_sold
FROM dbo.sales
GROUP BY product_name
ORDER BY total_sales ASC;

-- Finding: the bottom 10 products each sold under 10 in total, mostly
-- once. Results saved in outputs/bottom_10_products_sql_result.xlsx.
