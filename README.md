
# 🛒 Superstore Profitability Analysis

A data analytics project using **Snowflake SQL** and **Streamlit** to identify why a retail business is losing money on specific products and discount tiers.

## 🎯 Key Insight

**Discounts above 20% systematically destroy profit.**

| Discount Tier   | Orders | Profit       | Margin    |
|-----------------|--------|--------------|-----------|
| 0% (no discount)| 4,798  | **+$320,988**| **+29.5%**|
| 1–20%           | 3,803  | +$100,786    | +11.9%    |
| 21–40%          | 460    | -$35,818     | -15.3%    |
| 41–60%          | 215    | -$28,944     | -40.7%    |
| 60%+ (heavy)    | 718    | **-$70,615** | **-122.6%**|

Two sub-categories — **Tables** and **Bookcases** — run average discounts above 21%, making them structurally unprofitable. Eliminating discounts above 20% on these items could recover an estimated **$21K+ in profit**.

## 🛠 Tech Stack

- **Snowflake** — cloud data warehouse
- **SQL** — analytical queries with CTEs, window functions, and `QUALIFY`
- **Streamlit in Snowflake** — interactive dashboard
- **Python (pandas)** — light data wrangling

## 📊 Dashboard

The dashboard surfaces four areas of insight:
1. **KPIs** — total orders, revenue, profit, margin
2. **Discount Cliff** — visual proof that profit drops sharply above 20% discount
3. **Sub-Category Winners & Losers** — Tables, Bookcases, Supplies bleed money; Copiers and Paper deliver 30%+ margins
4. **Regional Performance** — comparing North, South, East, West

## 📁 Project Structure```
.
├── README.md
├── sql/
│   ├── 01_setup.sql          # Database, schema, table, stage creation
│   ├── 02_load_data.sql      # COPY INTO command
│   └── 03_analytics.sql      # Analytical queries
├── streamlit_app.py          # Dashboard code
└── screenshots/
    └── dashboard.png
```

## 🚀 Running This Project Yourself

1. Sign up for a free [Snowflake trial](https://signup.snowflake.com)
2. Download the [Superstore dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final) from Kaggle
3. Run `sql/01_setup.sql` to create the database, schema, table, and stage
4. Upload the CSV to the stage via Snowsight
5. Run `sql/02_load_data.sql` to load the data
6. Run queries from `sql/03_analytics.sql` to explore
7. Create a Streamlit-in-Snowflake app, paste in `streamlit_app.py`, and run

## 📚 What I Learned

- Setting up a Snowflake environment from scratch (warehouse, database, stages, file formats)
- Loading CSV data via `COPY INTO` and debugging column mismatches
- Writing analytical SQL with `CASE`, window functions, and Snowflake's `QUALIFY` clause
- Building interactive dashboards with Streamlit-in-Snowflake using `get_active_session()`
- Translating raw query output into a clear business recommendation
