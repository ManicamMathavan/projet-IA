"""Time-aware validation helpers."""

import pandas as pd


def temporal_split(
    data: pd.DataFrame,
    date_column: str = "Date",
    validation_days: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split chronologically, keeping the last ``validation_days`` for validation."""
    if validation_days <= 0 or validation_days >= len(data):
        raise ValueError("validation_days must be between 1 and len(data) - 1")
    ordered = data.sort_values(date_column).reset_index(drop=True)
    return ordered.iloc[:-validation_days].copy(), ordered.iloc[-validation_days:].copy()
