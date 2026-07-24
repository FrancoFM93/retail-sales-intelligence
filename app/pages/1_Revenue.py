import sys
from pathlib import Path

# This page is one directory deeper than Home.py: pages -> app -> repository root.
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from src.data_loader import load_all
from src.transforms import build_full_df, get_monthly_revenue

st.set_page_config(page_title="Revenue Analysis", page_icon="📈", layout="wide")


@st.cache_data
def load():
    # Cache the prepared frames because changing a widget reruns this page.
    customers, orders, order_items, payments = load_all()
    df_full = build_full_df(orders, payments, customers)
    return df_full, get_monthly_revenue(df_full)


df_full, monthly_revenue = load()

st.title("📈 Revenue Analysis")
st.caption("Revenue = payment value from delivered orders. Sparse September–October 2018 data is excluded.")
st.divider()

# --- Filters ---
years = sorted(df_full["order_purchase_timestamp"].dt.year.unique())
# A Streamlit widget returns its current value. Changing it triggers a rerun
# and the new list is used by the mask below.
selected_years = st.multiselect("Filter by year", years, default=years)

if not selected_years:
    # Stop before max(), mean(), and plotting receive an empty DataFrame.
    st.info("Select at least one year to display the revenue analysis.")
    st.stop()

mask = df_full["order_purchase_timestamp"].dt.year.isin(selected_years)
filtered = get_monthly_revenue(df_full[mask])
peak = filtered.loc[filtered["payment_value"].idxmax()]

# --- Chart ---
fig, ax = plt.subplots(figsize=(12, 4))
ax.fill_between(filtered["month"], filtered["payment_value"], alpha=0.2, color="#1f77b4")
ax.plot(filtered["month"], filtered["payment_value"], color="#1f77b4", linewidth=2)
ax.set_title("Delivered-Order Payment Value by Month", fontsize=14, fontweight="bold")
ax.set_xlabel("")
ax.set_ylabel("Revenue (R$)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"R${x:,.0f}"))
# Show one date label per quarter instead of labeling every month.
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))
ax.grid(axis="y", linestyle="--", alpha=0.5)
fig.tight_layout()
st.pyplot(fig, width="stretch")

st.divider()

# --- Stats ---
col1, col2, col3 = st.columns(3)
col1.metric(
    "Peak Month",
    f"{peak['month']:%b %Y}",
    delta=f"R$ {peak['payment_value']:,.0f}",
    delta_color="off",
)
col2.metric("Avg Monthly Revenue", f"R$ {filtered['payment_value'].mean():,.0f}")
col3.metric("Total (filtered)", f"R$ {filtered['payment_value'].sum():,.0f}")

revenue_2018 = monthly_revenue[monthly_revenue["month"].dt.year.eq(2018)]
if 2018 in selected_years:
    st.subheader("Key Takeaway")
    st.info(
        "From January through August 2018, monthly delivered-order payment value "
        fr"ranged from **R\$ {revenue_2018['payment_value'].min():,.0f}** to "
        fr"**R\$ {revenue_2018['payment_value'].max():,.0f}**. The monthly average "
        fr"was **R\$ {revenue_2018['payment_value'].mean():,.0f}**."
    )
else:
    st.info(
        f"The selected period peaked in **{peak['month']:%B %Y}** at "
        f"**R$ {peak['payment_value']:,.0f}**."
    )
st.caption(
    "Interpretation: the chart establishes timing and scale, but the available "
    "tables do not identify promotions or other causes of monthly changes."
)

# --- Table ---
with st.expander("Monthly breakdown"):
    display = filtered.copy()
    display["month"] = display["month"].dt.strftime("%Y-%m")
    display["payment_value"] = display["payment_value"].map("R$ {:,.2f}".format)
    display.columns = ["Month", "Revenue"]
    st.dataframe(display, width="stretch", hide_index=True)
