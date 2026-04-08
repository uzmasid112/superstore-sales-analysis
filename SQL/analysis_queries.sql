-- ── QUERY 1: Total revenue and orders ────────────────────────────────
SELECT
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS total_revenue,
    COUNT(*) AS total_rows,
    ROUND(AVG(sales), 2) AS avg_sale_per_row
FROM sales;

-- ── QUERY 2: Revenue by region ───────────────────────────────────────
SELECT
    region,
    ROUND(SUM(sales), 2) AS total_sales,
    COUNT(*) AS row_count,
    COUNT(DISTINCT order_id) AS order_count
FROM sales
GROUP BY region
ORDER BY total_sales DESC;

-- ── QUERY 3: Top 10 best-selling products ────────────────────────────
SELECT TOP 10
    product_name,
    ROUND(SUM(sales), 2) AS total_sales,
    COUNT(*) AS times_sold,
    COUNT(DISTINCT order_id) AS order_count
FROM sales
GROUP BY product_name
ORDER BY total_sales DESC;

-- ── QUERY 4: Monthly sales trend ─────────────────────────────────────
SELECT
    FORMAT(CAST(order_date AS datetime), 'yyyy-MM') AS month,
    ROUND(SUM(sales), 2) AS monthly_sales,
    COUNT(DISTINCT order_id) AS monthly_orders
FROM sales
GROUP BY FORMAT(CAST(order_date AS datetime), 'yyyy-MM')
ORDER BY month;

-- ── QUERY 5: Sales by category and sub-category ──────────────────────
SELECT
    category,
    sub_category,
    ROUND(SUM(sales), 2) AS total_sales,
    COUNT(*) AS row_count,
    COUNT(DISTINCT order_id) AS order_count
FROM sales
GROUP BY category, sub_category
ORDER BY category, total_sales DESC;

-- ── QUERY 6: Bottom 10 lowest-selling products ───────────────────────
SELECT TOP 10
    product_name,
    ROUND(SUM(sales), 2) AS total_sales,
    COUNT(*) AS times_sold
FROM sales
GROUP BY product_name
ORDER BY total_sales ASC;