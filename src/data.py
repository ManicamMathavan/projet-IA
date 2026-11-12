"""Loading utilities for the Rossmann datasets."""

from pathlib import Path

import pandas as pd


def load_raw_data(data_dir: str | Path = "data/raw") -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load train, test and store CSV files from ``data_dir``."""
    data_path = Path(data_dir)
    paths = {name: data_path / f"{name}.csv" for name in ("train", "test", "store")}
    missing = [str(path) for path in paths.values() if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing Kaggle files: {', '.join(missing)}")

    return tuple(pd.read_csv(paths[name]) for name in ("train", "test", "store"))


def merge_store(
    sales: pd.DataFrame, store: pd.DataFrame
) -> pd.DataFrame:
    """Join sales data with store metadata without mutating either input."""
    if "Store" not in sales or "Store" not in store:
        raise KeyError("Both dataframes must contain the 'Store' column")
    return sales.merge(store, on="Store", how="left", validate="many_to_one")
