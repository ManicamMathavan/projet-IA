"""Model factories used by the training pipeline."""

from typing import Any

from lightgbm import LGBMRegressor


def make_lgbm_regressor(seed: int = 42, **kwargs: Any) -> LGBMRegressor:
    """Create the team's baseline LightGBM regressor."""
    parameters = {
        "n_estimators": 500,
        "learning_rate": 0.05,
        "num_leaves": 31,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "random_state": seed,
        "verbosity": -1,
    }
    parameters.update(kwargs)
    return LGBMRegressor(**parameters)
