import pandas as pd
from pathlib import Path

# Build the data path from this module's location instead of the current
# working directory, so loading still works when Streamlit starts from elsewhere.
DATA_DIR = Path(__file__).parent.parent / "data" / "raw"


def load_customers() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "olist_customers_dataset.csv")


def load_orders() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "olist_orders_dataset.csv")
    # Pandas initially reads the timestamp as text. Converting it once here
    # enables the .dt date operations used by every downstream analysis.
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    return df


def load_order_items() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "olist_order_items_dataset.csv")


def load_payments() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "olist_order_payments_dataset.csv")


def load_all() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    # Callers unpack this tuple positionally, so this return order is part
    # of the function's contract.
    return load_customers(), load_orders(), load_order_items(), load_payments()
