"""Competition metrics."""

import numpy as np


def rmspe(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Return RMSPE, ignoring zero-sales rows as Kaggle does."""
    actual = np.asarray(y_true, dtype=float)
    predicted = np.asarray(y_pred, dtype=float)
    mask = actual != 0
    if not np.any(mask):
        raise ValueError("RMSPE is undefined when all actual values are zero")
    return float(np.sqrt(np.mean(((actual[mask] - predicted[mask]) / actual[mask]) ** 2)))
