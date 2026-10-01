# Product Analytics Dashboard

A small portfolio project demonstrating practical skills for a Data Analyst / Product Analytics role.

## What this project demonstrates

- SQL queries on a relational SQLite database
- KPI calculation: revenue, orders, average order value, units sold
- Python data analysis with pandas
- Data visualization with matplotlib and Streamlit
- Filtering by region and channel
- Trend and product/region analysis
- Basic anomaly detection
- Data quality checks
- Reporting-oriented project structure

## Project structure

```text
product-analytics-dashboard/
├── data/
│   ├── orders.csv
│   └── analytics.db
├── sql/
│   ├── 01_kpis.sql
│   ├── 02_revenue_by_product.sql
│   ├── 03_revenue_by_region.sql
│   ├── 04_monthly_trend.sql
│   └── 05_anomalies.sql
├── src/
│   ├── analysis.py
│   └── dashboard.py
├── reports/
├── requirements.txt
└── README.md
```

## How to run

```bash
pip install -r requirements.txt
python src/analysis.py
streamlit run src/dashboard.py
```

The dashboard opens locally in your browser.

## Example business questions

1. How much revenue was generated?
2. Which products generate the most revenue?
3. Which regions generate the most revenue?
4. How does revenue change over time?
5. Which orders look unusual?
6. Does the dataset contain missing, duplicated, or invalid values?

## Skills shown

**SQL:** aggregation, GROUP BY, CTEs, filtering, ordering

**Python:** pandas, SQLite, basic statistics, data quality checks

**Visualization:** matplotlib, Streamlit charts

**Analytics:** KPIs, trends, segmentation, anomaly detection

## Possible next step

The same dashboard could later be connected to PostgreSQL and a BI tool such as Metabase, Tableau, or Looker.
