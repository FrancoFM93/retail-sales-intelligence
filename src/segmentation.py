import pandas as pd


def compute_rfm(
    orders: pd.DataFrame, payments: pd.DataFrame, customers: pd.DataFrame
) -> pd.DataFrame:
    df = (
        orders.merge(payments, on="order_id")
        .merge(customers, on="customer_id")
    )
    snapshot = df["order_purchase_timestamp"].max()

    rfm = (
        df.groupby("customer_unique_id")
        .agg(
            recency=("order_purchase_timestamp", lambda x: (snapshot - x.max()).days),
            frequency=("order_id", "nunique"),
            monetary=("payment_value", "sum"),
        )
        .reset_index()
    )

    rfm["R_score"] = pd.qcut(
        rfm["recency"], 5, labels=[5, 4, 3, 2, 1], duplicates="drop"
    ).astype(int)
    rfm["F_score"] = pd.qcut(
        rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]
    ).astype(int)
    rfm["M_score"] = pd.qcut(
        rfm["monetary"], 5, labels=[1, 2, 3, 4, 5], duplicates="drop"
    ).astype(int)

    rfm["segment"] = rfm.apply(_segment_customer, axis=1)
    return rfm


def _segment_customer(row: pd.Series) -> str:
    if row["R_score"] == 5 and row["F_score"] >= 4:
        return "VIP"
    elif row["F_score"] >= 4:
        return "Loyal"
    elif row["R_score"] <= 2:
        return "At Risk"
    else:
        return "Regular"
