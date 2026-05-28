# Superstore Profitability Dashboard
import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session

# Page config
st.set_page_config(page_title="Superstore Analytics", layout="wide")

# Get Snowflake session and set context
session = get_active_session()
session.sql("USE DATABASE retail_db").collect()
session.sql("USE SCHEMA analytics").collect()

# Title
st.title("🛒 Superstore Profitability Analysis")
st.markdown("**Key insight:** Discounts above 20% destroy profit. Three sub-categories run unprofitable due to discount discipline issues.")

# ============ TOP KPIs ============
kpi_query = """
SELECT 
  COUNT(*) AS total_orders,
  SUM(sales) AS total_revenue,
  SUM(profit) AS total_profit,
  ROUND(SUM(profit) / SUM(sales) * 100, 2) AS margin_pct
FROM orders
"""
kpis = session.sql(kpi_query).to_pandas()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Orders", f"{int(kpis['TOTAL_ORDERS'][0]):,}")
col2.metric("Revenue", f"${kpis['TOTAL_REVENUE'][0]:,.0f}")
col3.metric("Profit", f"${kpis['TOTAL_PROFIT'][0]:,.0f}")
col4.metric("Margin", f"{kpis['MARGIN_PCT'][0]}%")

st.divider()

# ============ DISCOUNT TIER ANALYSIS ============
st.subheader("💸 The Discount Cliff: When Discounts Destroy Profit")

discount_query = """
SELECT 
  CASE 
    WHEN discount = 0 THEN '0% (no discount)'
    WHEN discount <= 0.2 THEN '1-20%'
    WHEN discount <= 0.4 THEN '21-40%'
    WHEN discount <= 0.6 THEN '41-60%'
    ELSE '60%+ (heavy)'
  END AS discount_tier,
  COUNT(*) AS orders,
  SUM(sales) AS revenue,
  SUM(profit) AS profit,
  ROUND(SUM(profit) / SUM(sales) * 100, 2) AS margin_pct
FROM orders
GROUP BY discount_tier
ORDER BY MIN(discount)
"""
discount_df = session.sql(discount_query).to_pandas()

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Profit by Discount Tier**")
    st.bar_chart(discount_df.set_index('DISCOUNT_TIER')['PROFIT'])
with col2:
    st.markdown("**Margin % by Discount Tier**")
    st.bar_chart(discount_df.set_index('DISCOUNT_TIER')['MARGIN_PCT'])

st.dataframe(discount_df, use_container_width=True, hide_index=True)

st.divider()

# ============ SUB-CATEGORY PROFITABILITY ============
st.subheader("📦 Sub-Category Profitability: Winners & Losers")

subcat_query = """
SELECT 
  sub_category,
  SUM(sales) AS revenue,
  SUM(profit) AS profit,
  ROUND(SUM(profit) / SUM(sales) * 100, 2) AS margin_pct,
  ROUND(AVG(discount) * 100, 1) AS avg_discount_pct
FROM orders
GROUP BY sub_category
ORDER BY profit ASC
"""
subcat_df = session.sql(subcat_query).to_pandas()

col1, col2 = st.columns(2)
with col1:
    st.markdown("**🔴 Top 5 Loss-Makers**")
    losers = subcat_df.head(5)
    st.bar_chart(losers.set_index('SUB_CATEGORY')['PROFIT'])
with col2:
    st.markdown("**🟢 Top 5 Profit-Makers**")
    winners = subcat_df.tail(5).iloc[::-1]
    st.bar_chart(winners.set_index('SUB_CATEGORY')['PROFIT'])

st.markdown("**Full breakdown:**")
st.dataframe(subcat_df, use_container_width=True, hide_index=True)

st.divider()

# ============ REGIONAL PERFORMANCE ============
st.subheader("🗺️ Regional Performance")

region_query = """
SELECT 
  region,
  COUNT(*) AS orders,
  SUM(sales) AS revenue,
  SUM(profit) AS profit,
  ROUND(SUM(profit) / SUM(sales) * 100, 2) AS margin_pct
FROM orders
GROUP BY region
ORDER BY profit DESC
"""
region_df = session.sql(region_query).to_pandas()

col1, col2 = st.columns(2)
with col1:
    st.bar_chart(region_df.set_index('REGION')['REVENUE'])
    st.caption("Revenue by Region")
with col2:
    st.bar_chart(region_df.set_index('REGION')['PROFIT'])
    st.caption("Profit by Region")

st.dataframe(region_df, use_container_width=True, hide_index=True)

st.divider()

# ============ THE INSIGHT ============
st.subheader("💡 The Recommendation")
st.info("""
**Stop discounting Tables and Bookcases above 20%.**

These two sub-categories alone leak **~$21,000 in profit** on $322,000 in revenue,  
while items with strict discount discipline like Copiers run **37% margins**.

The 20% discount threshold is where unit economics break — every tier above it loses money.
""")
