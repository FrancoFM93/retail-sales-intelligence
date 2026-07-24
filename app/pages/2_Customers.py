import sys
from pathlib import Path

# This page is one directory deeper than Home.py: pages -> app -> repository root.
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from src.data_loader import load_all
from src.transforms import build_full_df, get_customer_revenue, get_pareto, get_items_per_order

st.set_page_config(page_title="Customer Analysis", page_icon="👥", layout="wide")


@st.cache_data
def load():
    # Cache the prepared customer and basket frames across widget reruns.
    customers, orders, order_items, payments = load_all()
    df_full = build_full_df(orders, payments, customers)
    customer_revenue = get_customer_revenue(df_full)
    pareto = get_pareto(customer_revenue)
    items = get_items_per_order(order_items, df_full["order_id"].drop_duplicates())
    return customer_revenue, pareto, items


customer_revenue, pareto, items_per_order = load()

st.title("👥 Customer Analysis")
st.caption("Customer value is based on payment value from delivered orders through August 2018.")
st.divider()

# --- Pareto ---
st.subheader("Pareto: Revenue Concentration")

target = st.slider("Revenue target (%)", min_value=50, max_value=95, value=80, step=5)
# The frame is sorted by customer revenue, so the first matching row tells us
# how much of the customer base is needed to reach the selected target.
threshold = pareto[pareto["cumulative_pct"] >= target].iloc[0]
pct_customers = threshold["customer_pct"]

col1, col2 = st.columns([3, 1])

with col1:
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(pareto["customer_pct"], pareto["cumulative_pct"], color="#1f77b4", linewidth=2)
    ax.axhline(target, color="red", linestyle="--", linewidth=1, label=f"{target}% revenue")
    ax.axvline(pct_customers, color="orange", linestyle="--", linewidth=1,
               label=f"{pct_customers:.1f}% customers")
    ax.fill_between(pareto["customer_pct"], pareto["cumulative_pct"], alpha=0.1, color="#1f77b4")
    ax.set_xlabel("% of Customers (ranked by revenue)")
    ax.set_ylabel("Cumulative % of Revenue")
    ax.set_title("Cumulative Revenue Distribution", fontweight="bold")
    ax.xaxis.set_major_formatter(mticker.PercentFormatter(xmax=100))
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=100))
    ax.legend()
    ax.grid(linestyle="--", alpha=0.4)
    fig.tight_layout()
    st.pyplot(fig, width="stretch")

with col2:
    st.metric(f"Customers to reach {target}% revenue", f"{pct_customers:.1f}%")
    st.metric("Total unique customers", f"{len(pareto):,}")
    st.metric("Top 10% customers revenue share",
              f"{pareto[pareto['customer_pct'] <= 10]['payment_value'].sum() / pareto['payment_value'].sum() * 100:.1f}%")

st.subheader("Business Interpretation")
st.info(
    f"Revenue is less concentrated than a classic 80/20 pattern: "
    f"**{pct_customers:.1f}% of customers generate {target}% of revenue**, while "
    f"the top 10% generate **{pareto[pareto['customer_pct'] <= 10]['payment_value'].sum() / pareto['payment_value'].sum() * 100:.1f}%**."
)
st.caption(
    "This supports broad customer engagement alongside targeted high-value campaigns; "
    "it does not show which campaign would produce incremental revenue."
)

st.divider()

# --- Items per order ---
st.subheader("Items per Order Distribution")

fig2, ax2 = plt.subplots(figsize=(10, 3))
cap = st.slider("Cap item count at", min_value=5, max_value=20, value=10)
# Clipping combines all larger baskets into the final visible bin. This keeps
# rare outliers from making the common one- and two-item orders unreadable.
capped = items_per_order["item_count"].clip(upper=cap)
ax2.hist(capped, bins=range(1, cap + 2), edgecolor="white", color="#1f77b4", align="left")
ax2.set_xlabel("Items per Order")
ax2.set_ylabel("Number of Orders")
ax2.set_title("Distribution of Items per Order", fontweight="bold")
ticks = list(range(1, cap + 1))
ax2.set_xticks(ticks)
# The plus sign makes the information loss from clipping explicit.
ax2.set_xticklabels([str(value) for value in ticks[:-1]] + [f"{cap}+"])
ax2.grid(axis="y", linestyle="--", alpha=0.4)
fig2.tight_layout()
st.pyplot(fig2, width="stretch")

col3, col4, col5 = st.columns(3)
col3.metric("Avg items per order", f"{items_per_order['item_count'].mean():.2f}")
col4.metric("Orders with 1 item", f"{(items_per_order['item_count'] == 1).sum() / len(items_per_order) * 100:.1f}%")
col5.metric("Max items in one order", f"{items_per_order['item_count'].max()}")

one_item_pct = items_per_order["item_count"].eq(1).mean() * 100
st.info(
    f"**{one_item_pct:.1f}% of orders contain one item.** Bundles or cross-selling "
    "are reasonable experiments to test, but this distribution alone does not prove "
    "that either would increase completed-order value."
)
