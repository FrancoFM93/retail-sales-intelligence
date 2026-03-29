import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from src.data_loader import load_all
from src.transforms import build_full_df, get_monthly_revenue, get_customer_revenue
from src.segmentation import compute_rfm

st.set_page_config(
    page_title="Retail Sales Intelligence",
    page_icon="🛒",
    layout="wide",
)


@st.cache_data
def load_data():
    customers, orders, order_items, payments = load_all()
    df_full = build_full_df(orders, payments, customers)
    monthly_revenue = get_monthly_revenue(df_full)
    customer_revenue = get_customer_revenue(df_full)
    rfm = compute_rfm(orders, payments, customers)
    return df_full, monthly_revenue, customer_revenue, rfm


df_full, monthly_revenue, customer_revenue, rfm = load_data()

st.title("🛒 Retail Sales Intelligence")
st.caption("Brazilian E-Commerce Dataset (Olist)")
st.divider()

total_revenue = df_full["payment_value"].sum()
total_orders = df_full["order_id"].nunique()
total_customers = df_full["customer_unique_id"].nunique()
avg_order_value = total_revenue / total_orders

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"R$ {total_revenue:,.0f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Unique Customers", f"{total_customers:,}")
col4.metric("Avg Order Value", f"R$ {avg_order_value:,.2f}")

st.divider()

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Revenue Trend")
    st.line_chart(monthly_revenue.set_index("month")["payment_value"], height=220)

with col_right:
    st.subheader("Revenue by Segment")
    rev_seg = (
        rfm.groupby("segment")["monetary"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    st.bar_chart(rev_seg.set_index("segment")["monetary"], height=220)

st.divider()
st.caption("Use the sidebar to explore Revenue, Customer, and Segmentation analyses.")
