import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "raw"


def load_customers() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "olist_customers_dataset.csv")


def load_orders() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "olist_orders_dataset.csv")
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    return df


def load_order_items() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "olist_order_items_dataset.csv")


def load_payments() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "olist_order_payments_dataset.csv")


def load_all() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    return load_customers(), load_orders(), load_order_items(), load_payments()
