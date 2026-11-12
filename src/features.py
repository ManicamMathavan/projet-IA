"""Pure feature engineering functions."""

import pandas as pd


def add_date_features(data: pd.DataFrame, date_column: str = "Date") -> pd.DataFrame:
    """Add calendar features and return a new dataframe."""
    if date_column not in data:
        raise KeyError(f"Missing date column: {date_column}")
    result = data.copy()
    dates = pd.to_datetime(result[date_column], dayfirst=True)
    result["year"] = dates.dt.year
    result["month"] = dates.dt.month
    result["week"] = dates.dt.isocalendar().week.astype("int16")
    result["day_of_month"] = dates.dt.day
    result["day_of_week"] = dates.dt.dayofweek
    result["is_weekend"] = (dates.dt.dayofweek >= 5).astype("int8")
    return result
