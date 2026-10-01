import sqlite3
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "analytics.db"
OUT = ROOT / "reports"
OUT.mkdir(exist_ok=True)

con = sqlite3.connect(DB)

monthly = pd.read_sql_query("""
SELECT
    strftime('%Y-%m', order_date) AS month,
    ROUND(SUM(revenue), 2) AS revenue
FROM orders
GROUP BY month
ORDER BY month
""", con)

product = pd.read_sql_query("""
SELECT
    product,
    ROUND(SUM(revenue), 2) AS revenue
FROM orders
GROUP BY product
ORDER BY revenue DESC
""", con)

# Revenue trend
plt.figure(figsize=(9, 5))
plt.plot(monthly["month"], monthly["revenue"], marker="o")
plt.title("Monthly Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUT / "monthly_revenue.png", dpi=150)
plt.close()

# Product performance
plt.figure(figsize=(9, 5))
plt.bar(product["product"], product["revenue"])
plt.title("Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Revenue")
plt.xticks(rotation=25, ha="right")
plt.tight_layout()
plt.savefig(OUT / "revenue_by_product.png", dpi=150)
plt.close()

# Data quality checks
orders = pd.read_sql_query("SELECT * FROM orders", con)
quality = {
    "row_count": len(orders),
    "duplicate_order_ids": int(orders["order_id"].duplicated().sum()),
    "missing_values": int(orders.isna().sum().sum()),
    "negative_revenue": int((orders["revenue"] < 0).sum()),
}
pd.DataFrame([quality]).to_csv(OUT / "data_quality_report.csv", index=False)

print("Analysis completed.")
print(pd.DataFrame([quality]).to_string(index=False))
con.close()
