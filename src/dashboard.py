import sqlite3
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "analytics.db"

st.set_page_config(
    page_title="Product Analytics Dashboard",
    layout="wide"
)

st.title("Product Analytics Dashboard")
st.caption("SQL + Python + KPI reporting + anomaly detection")

con = sqlite3.connect(DB)
df = pd.read_sql_query("SELECT * FROM orders", con)
con.close()

df["order_date"] = pd.to_datetime(df["order_date"])

st.sidebar.header("Filters")

regions = st.sidebar.multiselect(
    "Region",
    sorted(df["region"].unique()),
    default=sorted(df["region"].unique())
)

channels = st.sidebar.multiselect(
    "Channel",
    sorted(df["channel"].unique()),
    default=sorted(df["channel"].unique())
)

filtered = df[
    df["region"].isin(regions) &
    df["channel"].isin(channels)
].copy()

total_revenue = filtered["revenue"].sum()
orders = filtered["order_id"].nunique()
aov = filtered["revenue"].mean()
units = filtered["quantity"].sum()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Revenue", f"${total_revenue:,.0f}")
c2.metric("Orders", f"{orders:,}")
c3.metric("Avg. Order Value", f"${aov:,.2f}")
c4.metric("Units Sold", f"{units:,}")

st.divider()

# Revenue Trend
st.subheader("Revenue Trend")

monthly = (
    filtered
    .groupby(filtered["order_date"].dt.to_period("M"))["revenue"]
    .sum()
)

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(monthly.index.astype(str), monthly.values, marker="o")
ax.set_xlabel("Month")
ax.set_ylabel("Revenue")
ax.tick_params(axis="x", rotation=45)
fig.tight_layout()

st.pyplot(fig)

# Product and Region
col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue by Product")

    product = (
        filtered
        .groupby("product")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(product.index, product.values)
    ax.set_ylabel("Revenue")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()

    st.pyplot(fig)

with col2:
    st.subheader("Revenue by Region")

    region = (
        filtered
        .groupby("region")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(region.index, region.values)
    ax.set_ylabel("Revenue")
    fig.tight_layout()

    st.pyplot(fig)

# Anomalies
st.subheader("Potential Anomalies")

threshold = (
    filtered["revenue"].mean()
    + 2 * filtered["revenue"].std()
)

anomalies = (
    filtered[filtered["revenue"] > threshold]
    .sort_values("revenue", ascending=False)
)

st.write(
    f"Orders above the dynamic threshold of "
    f"**${threshold:,.2f}**:"
)

st.dataframe(
    anomalies[
        [
            "order_id",
            "order_date",
            "product",
            "region",
            "quantity",
            "revenue"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

# Data Quality
st.subheader("Data Quality")

quality = pd.DataFrame({
    "Check": [
        "Rows",
        "Duplicate Order IDs",
        "Missing Values",
        "Negative Revenue"
    ],
    "Result": [
        len(filtered),
        filtered["order_id"].duplicated().sum(),
        filtered.isna().sum().sum(),
        (filtered["revenue"] < 0).sum()
    ]
})

st.dataframe(
    quality,
    use_container_width=True,
    hide_index=True
)
