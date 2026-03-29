import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from src.data_loader import load_all
from src.transforms import build_full_df, get_monthly_revenue

st.set_page_config(page_title="Revenue Analysis", page_icon="📈", layout="wide")


@st.cache_data
def load():
    customers, orders, order_items, payments = load_all()
    df_full = build_full_df(orders, payments, customers)
    return df_full, get_monthly_revenue(df_full)


df_full, monthly_revenue = load()

st.title("📈 Revenue Analysis")
st.divider()

# --- Filters ---
years = sorted(df_full["order_purchase_timestamp"].dt.year.unique())
selected_years = st.multiselect("Filter by year", years, default=years)

mask = df_full["order_purchase_timestamp"].dt.year.isin(selected_years)
filtered = get_monthly_revenue(df_full[mask])

# --- Chart ---
fig, ax = plt.subplots(figsize=(12, 4))
ax.fill_between(filtered["month"], filtered["payment_value"], alpha=0.2, color="#1f77b4")
ax.plot(filtered["month"], filtered["payment_value"], color="#1f77b4", linewidth=2)
ax.set_title("Monthly Revenue", fontsize=14, fontweight="bold")
ax.set_xlabel("")
ax.set_ylabel("Revenue (R$)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R${x:,.0f}"))
ax.grid(axis="y", linestyle="--", alpha=0.5)
fig.tight_layout()
st.pyplot(fig)

st.divider()

# --- Stats ---
col1, col2, col3 = st.columns(3)
col1.metric("Peak Month Revenue", f"R$ {filtered['payment_value'].max():,.0f}")
col2.metric("Avg Monthly Revenue", f"R$ {filtered['payment_value'].mean():,.0f}")
col3.metric("Total (filtered)", f"R$ {filtered['payment_value'].sum():,.0f}")

# --- Table ---
with st.expander("Monthly breakdown"):
    display = filtered.copy()
    display["month"] = display["month"].dt.strftime("%Y-%m")
    display["payment_value"] = display["payment_value"].map("R$ {:,.2f}".format)
    display.columns = ["Month", "Revenue"]
    st.dataframe(display, use_container_width=True, hide_index=True)
