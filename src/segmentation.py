import pandas as pd

from src.transforms import ANALYSIS_CUTOFF, get_analysis_orders


def compute_rfm(
    orders: pd.DataFrame, payments: pd.DataFrame, customers: pd.DataFrame
) -> pd.DataFrame:
    # Payment rows may repeat an order, but grouping by the stable
    # customer_unique_id below restores one row per real customer.
    df = (
        get_analysis_orders(orders)
        .merge(payments, on="order_id")
        .merge(customers, on="customer_id")
    )
    # A fixed reference date makes recency reproducible and consistent with
    # the first day excluded by the analysis cutoff.
    snapshot = ANALYSIS_CUTOFF

    # The output grain changes from payment row to one row per unique customer.
    rfm = (
        df.groupby("customer_unique_id")
        .agg(
            recency=("order_purchase_timestamp", lambda x: (snapshot - x.max()).days),
            frequency=("order_id", "nunique"),
            monetary=("payment_value", "sum"),
        )
        .reset_index()
    )

    # Lower recency is better, so the most recent quintile receives score 5.
    # Monetary uses the normal direction: larger totals receive larger scores.
    rfm["R_score"] = pd.qcut(
        rfm["recency"], 5, labels=[5, 4, 3, 2, 1], duplicates="drop"
    ).astype(int)
    # Frequency scores reflect actual order counts: 1, 2, 3, 4, or 5+.
    # This avoids assigning artificial high scores to tied one-time buyers.
    rfm["F_score"] = rfm["frequency"].clip(upper=5).astype(int)
    rfm["M_score"] = pd.qcut(
        rfm["monetary"], 5, labels=[1, 2, 3, 4, 5], duplicates="drop"
    ).astype(int)

    # axis=1 passes one customer row at a time to the business-rule function.
    rfm["segment"] = rfm.apply(_segment_customer, axis=1)
    return rfm


def _segment_customer(row: pd.Series) -> str:
    """Assign a transparent segment using repeat behavior, recency, and value.

    VIP: repeat buyer in the top two recency and monetary bands.
    Loyal: repeat buyer in the top three recency bands.
    At Risk: customer in the bottom two recency bands.
    Regular: all other customers, including one-time buyers.
    """
    if row["frequency"] >= 2 and row["R_score"] >= 4 and row["M_score"] >= 4:
        return "VIP"
    elif row["frequency"] >= 2 and row["R_score"] >= 3:
        return "Loyal"
    elif row["R_score"] <= 2:
        return "At Risk"
    else:
        return "Regular"
