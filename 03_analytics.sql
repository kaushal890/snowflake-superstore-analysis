-- ============================================================
-- 03_analytics.sql
-- Analytical queries that surface profitability insights
-- ============================================================

USE DATABASE retail_db;
USE SCHEMA analytics;

-- 1. Headline KPIs
SELECT 
  COUNT(*) AS total_orders,
  SUM(sales) AS total_revenue,
  SUM(profit) AS total_profit,
  ROUND(SUM(profit) / SUM(sales) * 100, 2) AS overall_margin_pct
FROM orders;

-- 2. Revenue and profit by category
SELECT 
  category,
  COUNT(*) AS orders,
  SUM(sales) AS revenue,
  SUM(profit) AS profit,
  ROUND(SUM(profit) / SUM(sales) * 100, 2) AS margin_pct
FROM orders
GROUP BY category
ORDER BY revenue DESC;

-- 3. Top 5 sub-categories within each category (window function + QUALIFY)
SELECT 
  category,
  sub_category,
  SUM(sales) AS revenue,
  SUM(profit) AS profit
FROM orders
GROUP BY category, sub_category
QUALIFY ROW_NUMBER() OVER (PARTITION BY category ORDER BY SUM(sales) DESC) <= 5
O
