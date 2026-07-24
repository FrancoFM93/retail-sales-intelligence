import pandas as pd


# These constants define the shared analytical population used by every page.
# The cutoff is exclusive, so September 1 itself is not included.
REVENUE_ORDER_STATUS = "delivered"
ANALYSIS_CUTOFF = pd.Timestamp("2018-09-01")


def get_analysis_orders(orders: pd.DataFrame) -> pd.DataFrame:
    """Return delivered orders from complete months through August 2018."""
    # .copy() keeps later changes to this filtered frame from modifying a
    # view backed by the original orders DataFrame.
    return orders[
        orders["order_status"].eq(REVENUE_ORDER_STATUS)
        & orders["order_purchase_timestamp"].lt(ANALYSIS_CUTOFF)
    ].copy()


def build_orders_payments(orders: pd.DataFrame, payments: pd.DataFrame) -> pd.DataFrame:
    # merge() uses an inner join by default. An order can have several payment
    # rows, so the output grain is payment record rather than one row per order.
    return get_analysis_orders(orders).merge(payments, on="order_id")


def build_full_df(
    orders: pd.DataFrame, payments: pd.DataFrame, customers: pd.DataFrame
) -> pd.DataFrame:
    # customer_id connects an order to its customer record. The resulting
    # customer_unique_id is later used to combine purchases by the same person.
    return build_orders_payments(orders, payments).merge(customers, on="customer_id")


def get_monthly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    # Convert timestamps to monthly periods before grouping so every payment
    # row from the same calendar month contributes to one monthly total.
    result = (
        df.copy()
        .assign(month=lambda x: x["order_purchase_timestamp"].dt.to_period("M"))
        .groupby("month")["payment_value"]
        .sum()
        .reset_index()
    )
    # Matplotlib works more naturally with timestamps than Period values.
    result["month"] = result["month"].dt.to_timestamp()
    return result


def get_customer_revenue(df_full: pd.DataFrame) -> pd.DataFrame:
    # Use customer_unique_id because customer_id identifies an order-level
    # customer record, not the same person across multiple purchases.
    return (
        df_full.groupby("customer_unique_id")["payment_value"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )


def get_pareto(customer_revenue: pd.DataFrame) -> pd.DataFrame:
    # customer_revenue is already sorted from highest to lowest. Copy it so
    # adding analytical columns does not change the caller's DataFrame.
    cr = customer_revenue.copy()
    total = cr["payment_value"].sum()
    # cumsum() creates the running revenue total; the index gives the running
    # customer count because the frame has a fresh zero-based index.
    cr["cumulative_pct"] = cr["payment_value"].cumsum() / total * 100
    cr["customer_pct"] = (cr.index + 1) / len(cr) * 100
    return cr


def get_items_per_order(
    order_items: pd.DataFrame, valid_order_ids: pd.Series | None = None
) -> pd.DataFrame:
    items = order_items
    if valid_order_ids is not None:
        # Match basket metrics to the same delivered-order population used
        # by the revenue analysis.
        items = items[items["order_id"].isin(valid_order_ids)]
    # Each input row is one item; group size therefore becomes items per order.
    return items.groupby("order_id").size().reset_index(name="item_count")
