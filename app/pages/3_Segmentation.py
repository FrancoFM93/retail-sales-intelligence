import sys
from pathlib import Path

# This page is one directory deeper than Home.py: pages -> app -> repository root.
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from src.data_loader import load_all
from src.segmentation import compute_rfm

st.set_page_config(page_title="RFM Segmentation", page_icon="🧠", layout="wide")

SEGMENT_COLORS = {
    "VIP": "#2ecc71",
    "Loyal": "#3498db",
    "Regular": "#f39c12",
    "At Risk": "#e74c3c",
}


@st.cache_data
def load():
    # RFM is the slowest transformation, so caching prevents recomputing it
    # whenever the user changes the segment selector.
    customers, orders, order_items, payments = load_all()
    return compute_rfm(orders, payments, customers)


rfm = load()

st.title("🧠 RFM Segmentation")
st.caption("Delivered orders through August 2018; recency is measured from September 1, 2018.")
with st.expander("How segments are defined"):
    st.markdown(
        """
        - **VIP:** repeat buyers in the top two recency and monetary bands.
        - **Loyal:** other repeat buyers in the top three recency bands.
        - **At Risk:** customers in the bottom two recency bands.
        - **Regular:** all remaining customers, including one-time buyers.
        """
    )
st.divider()

# --- Overview metrics ---
segment_counts = rfm["segment"].value_counts()
segment_revenue = rfm.groupby("segment")["monetary"].sum()
priority_segments = ["VIP", "Loyal"]
# Boolean means are proportions because True behaves like 1 and False like 0.
priority_customer_share = rfm["segment"].isin(priority_segments).mean() * 100
priority_revenue_share = (
    segment_revenue.reindex(priority_segments, fill_value=0).sum()
    / segment_revenue.sum()
    * 100
)

cols = st.columns(len(SEGMENT_COLORS))
for col, (seg, color) in zip(cols, SEGMENT_COLORS.items()):
    count = segment_counts.get(seg, 0)
    rev = segment_revenue.get(seg, 0)
    col.metric(
        label=seg,
        value=f"{count:,} customers",
        delta=f"R$ {rev:,.0f}",
        delta_color="off",
    )

st.subheader("Key Takeaway")
st.info(
    f"VIP and Loyal customers represent **{priority_customer_share:.1f}% of customers** "
    f"and **{priority_revenue_share:.1f}% of delivered-order payment value**. These "
    "segments are intentionally selective because every member is a repeat buyer."
)
st.caption(
    "At Risk identifies low-recency customers, not confirmed churn. Re-engagement "
    "campaigns should be treated as experiments and measured against a control group."
)

st.divider()

# --- Charts ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Customer Distribution")
    fig, ax = plt.subplots(figsize=(5, 4))
    segs = list(SEGMENT_COLORS.keys())
    counts = [segment_counts.get(s, 0) for s in segs]
    colors = [SEGMENT_COLORS[s] for s in segs]
    bars = ax.bar(segs, counts, color=colors, edgecolor="white")
    ax.bar_label(bars, fmt="{:,.0f}", padding=3)
    ax.set_ylabel("Customers")
    ax.set_title("Customers per Segment", fontweight="bold")
    ax.yaxis.set_major_formatter(mticker.StrMethodFormatter("{x:,.0f}"))
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()
    st.pyplot(fig, width="stretch")

with col_right:
    st.subheader("Revenue by Segment")
    fig2, ax2 = plt.subplots(figsize=(5, 4))
    revenues = [segment_revenue.get(s, 0) for s in segs]
    bars2 = ax2.bar(segs, revenues, color=colors, edgecolor="white")
    ax2.bar_label(bars2, fmt="R${:,.0f}", padding=3, fontsize=8)
    ax2.set_ylabel("Revenue (R$)")
    ax2.set_title("Revenue per Segment", fontweight="bold")
    ax2.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda value, _: f"R${value / 1_000_000:.0f}M")
    )
    ax2.grid(axis="y", linestyle="--", alpha=0.4)
    fig2.tight_layout()
    st.pyplot(fig2, width="stretch")

st.divider()

# --- Scatter: Recency vs Monetary, colored by segment ---
st.subheader("Recency vs Monetary Value")

fig3, ax3 = plt.subplots(figsize=(10, 4))
for seg, color in SEGMENT_COLORS.items():
    subset = rfm[rfm["segment"] == seg]
    ax3.scatter(
        subset["recency"], subset["monetary"],
        c=color, label=seg, alpha=0.5, s=15, edgecolors="none"
    )
ax3.set_xlabel("Recency (days since last purchase)")
ax3.set_ylabel("Monetary Value (R$, log scale)")
# A log scale compresses large monetary outliers while keeping low-value
# customers visible. Equal vertical distances represent ratios, not differences.
ax3.set_yscale("log")
ax3.yaxis.set_major_formatter(mticker.FuncFormatter(lambda value, _: f"R${value:,.0f}"))
ax3.set_title("Customer Scatter by Segment", fontweight="bold")
ax3.legend()
ax3.grid(linestyle="--", alpha=0.3)
fig3.tight_layout()
st.pyplot(fig3, width="stretch")

st.divider()

# --- Drill-down table ---
st.subheader("Explore Segment")
selected = st.selectbox("Select segment", list(SEGMENT_COLORS.keys()))
# The selector triggers a rerun; this filter then rebuilds the displayed table
# for only the chosen segment.
subset = rfm[rfm["segment"] == selected][
    ["customer_unique_id", "recency", "frequency", "monetary", "R_score", "F_score", "M_score"]
].sort_values("monetary", ascending=False)

display_subset = subset.copy()
display_subset["monetary"] = display_subset["monetary"].map("R${:,.2f}".format)
display_subset["recency"] = display_subset["recency"].map("{:.0f} days".format)

st.dataframe(
    display_subset,
    width="stretch",
    hide_index=True,
)
