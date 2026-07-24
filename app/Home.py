import sys
from pathlib import Path

# Streamlit runs this file from app/, so add the repository root before
# importing the local src package.
sys.path.insert(0, str(Path(__file__).parent.parent))

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import streamlit as st
from src.data_loader import load_all
from src.transforms import (
    build_full_df,
    get_customer_revenue,
    get_monthly_revenue,
    get_pareto,
)
from src.segmentation import compute_rfm

st.set_page_config(
    page_title="Retail Sales Intelligence",
    page_icon="🛒",
    layout="wide",
)


@st.cache_data
def load_data():
    # Streamlit reruns this script after interactions. Caching avoids reading
    # and transforming the same CSV files on every rerun.
    customers, orders, order_items, payments = load_all()
    df_full = build_full_df(orders, payments, customers)
    monthly_revenue = get_monthly_revenue(df_full)
    customer_revenue = get_customer_revenue(df_full)
    rfm = compute_rfm(orders, payments, customers)
    return df_full, monthly_revenue, customer_revenue, rfm


df_full, monthly_revenue, customer_revenue, rfm = load_data()

st.title("🛒 Retail Sales Intelligence")
st.caption("Brazilian E-Commerce Dataset (Olist)")
st.caption("Revenue = payment value from delivered orders; trend period ends August 2018.")
st.divider()

total_revenue = df_full["payment_value"].sum()
# Payment rows can repeat an order, so orders and customers use distinct counts.
total_orders = df_full["order_id"].nunique()
total_customers = df_full["customer_unique_id"].nunique()
avg_order_value = total_revenue / total_orders
pareto = get_pareto(customer_revenue)
# Select the first point where cumulative revenue reaches the 80% threshold.
customers_for_80 = pareto.loc[pareto["cumulative_pct"].ge(80), "customer_pct"].iloc[0]
repeat_customer_pct = rfm["frequency"].gt(1).mean() * 100
analysis_period = (
    f"{df_full['order_purchase_timestamp'].min():%b %Y} – "
    f"{df_full['order_purchase_timestamp'].max():%b %Y}"
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Delivered Payment Value", f"R$ {total_revenue:,.0f}")
col2.metric("Delivered Orders", f"{total_orders:,}")
col3.metric("Customers", f"{total_customers:,}")
col4.metric("Average Order Value", f"R$ {avg_order_value:,.2f}")

col5, col6, col7 = st.columns(3)
col5.metric("Customers for 80% of Revenue", f"{customers_for_80:.1f}%")
col6.metric("Repeat Customers", f"{repeat_customer_pct:.1f}%")
col7.metric("Analysis Period", analysis_period)

st.subheader("Executive Summary")
st.info(
    f"Delivered orders generated **R$ {total_revenue / 1_000_000:.1f}M** in payment "
    f"value. Revenue is broadly distributed - **{customers_for_80:.1f}%** of customers "
    "generate 80% - while only "
    f"**{repeat_customer_pct:.1f}%** purchased more than once."
)
st.caption(
    "Potential action: test repeat-purchase and retention offers across the broader "
    "customer base; the historical data does not establish which intervention will work."
)

st.divider()

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Monthly Revenue")
    fig, ax = plt.subplots(figsize=(7, 3.2))
    ax.plot(
        monthly_revenue["month"],
        monthly_revenue["payment_value"],
        color="#1f77b4",
        linewidth=2,
    )
    ax.fill_between(
        monthly_revenue["month"],
        monthly_revenue["payment_value"],
        color="#1f77b4",
        alpha=0.12,
    )
    ax.set_xlabel("")
    ax.set_ylabel("Payment Value (R$)")
    ax.yaxis.set_major_formatter(
        # FuncFormatter receives each raw tick value and returns display text.
        mticker.FuncFormatter(lambda value, _: f"R${value / 1_000_000:.1f}M")
    )
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    fig.tight_layout()
    st.pyplot(fig, width="stretch")

with col_right:
    st.subheader("Revenue by Segment")
    rev_seg = (
        # RFM already has one row per customer, so summing monetary by segment
        # produces segment-level payment value without duplicating customers.
        rfm.groupby("segment")["monetary"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    segment_colors = {
        "VIP": "#2ecc71",
        "Loyal": "#3498db",
        "Regular": "#f39c12",
        "At Risk": "#e74c3c",
    }
    fig2, ax2 = plt.subplots(figsize=(7, 3.2))
    bars = ax2.bar(
        rev_seg["segment"],
        rev_seg["monetary"],
        color=[segment_colors[segment] for segment in rev_seg["segment"]],
    )
    ax2.bar_label(
        bars,
        labels=[f"R${value / 1_000_000:.1f}M" for value in rev_seg["monetary"]],
        padding=3,
        fontsize=9,
    )
    ax2.set_xlabel("")
    ax2.set_ylabel("Payment Value (R$)")
    ax2.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda value, _: f"R${value / 1_000_000:.0f}M")
    )
    ax2.grid(axis="y", linestyle="--", alpha=0.35)
    fig2.tight_layout()
    st.pyplot(fig2, width="stretch")

st.divider()
st.caption("Use the sidebar to explore Revenue, Customer, and Segmentation analyses.")
