import pandas as pd


def build_orders_payments(orders: pd.DataFrame, payments: pd.DataFrame) -> pd.DataFrame:
    return orders.merge(payments, on="order_id")


def build_full_df(
    orders: pd.DataFrame, payments: pd.DataFrame, customers: pd.DataFrame
) -> pd.DataFrame:
    return build_orders_payments(orders, payments).merge(customers, on="customer_id")


def get_monthly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    result = (
        df.copy()
        .assign(month=lambda x: x["order_purchase_timestamp"].dt.to_period("M"))
        .groupby("month")["payment_value"]
        .sum()
        .reset_index()
    )
    result["month"] = result["month"].dt.to_timestamp()
    return result


def get_customer_revenue(df_full: pd.DataFrame) -> pd.DataFrame:
    return (
        df_full.groupby("customer_unique_id")["payment_value"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )


def get_pareto(customer_revenue: pd.DataFrame) -> pd.DataFrame:
    cr = customer_revenue.copy()
    total = cr["payment_value"].sum()
    cr["cumulative_pct"] = cr["payment_value"].cumsum() / total * 100
    cr["customer_pct"] = (cr.index + 1) / len(cr) * 100
    return cr


def get_items_per_order(order_items: pd.DataFrame) -> pd.DataFrame:
    return order_items.groupby("order_id").size().reset_index(name="item_count")
