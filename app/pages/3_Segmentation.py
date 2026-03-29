import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
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
    customers, orders, order_items, payments = load_all()
    return compute_rfm(orders, payments, customers)


rfm = load()

st.title("🧠 RFM Segmentation")
st.divider()

# --- Overview metrics ---
segment_counts = rfm["segment"].value_counts()
segment_revenue = rfm.groupby("segment")["monetary"].sum()

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
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()
    st.pyplot(fig)

with col_right:
    st.subheader("Revenue by Segment")
    fig2, ax2 = plt.subplots(figsize=(5, 4))
    revenues = [segment_revenue.get(s, 0) for s in segs]
    bars2 = ax2.bar(segs, revenues, color=colors, edgecolor="white")
    ax2.bar_label(bars2, fmt="R${:,.0f}", padding=3, fontsize=8)
    ax2.set_ylabel("Revenue (R$)")
    ax2.set_title("Revenue per Segment", fontweight="bold")
    ax2.grid(axis="y", linestyle="--", alpha=0.4)
    fig2.tight_layout()
    st.pyplot(fig2)

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
ax3.set_ylabel("Monetary (R$)")
ax3.set_title("Customer Scatter by Segment", fontweight="bold")
ax3.legend()
ax3.grid(linestyle="--", alpha=0.3)
fig3.tight_layout()
st.pyplot(fig3)

st.divider()

# --- Drill-down table ---
st.subheader("Explore Segment")
selected = st.selectbox("Select segment", list(SEGMENT_COLORS.keys()))
subset = rfm[rfm["segment"] == selected][
    ["customer_unique_id", "recency", "frequency", "monetary", "R_score", "F_score", "M_score"]
].sort_values("monetary", ascending=False)

st.dataframe(
    subset.style.format({"monetary": "R${:,.2f}", "recency": "{:.0f} days"}),
    use_container_width=True,
    hide_index=True,
)
