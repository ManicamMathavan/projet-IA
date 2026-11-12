"""Command-line entry point for training and creating a submission."""

from pathlib import Path

import pandas as pd

from src.data import load_raw_data, merge_store
from src.features import add_date_features
from src.models import make_lgbm_regressor


def main() -> None:
    """Train a baseline model when the Kaggle files are available."""
    train, test, store = load_raw_data()
    train = add_date_features(merge_store(train, store))
    test = add_date_features(merge_store(test, store))
    target = "Sales"
    ignored = {"Date", target, "Customers"}
    columns = [
        column for column in train.select_dtypes(include="number").columns
        if column not in ignored
    ]
    if not columns:
        raise ValueError("No numeric features available for training")

    model = make_lgbm_regressor()
    model.fit(train[columns], train[target])
    predictions = model.predict(test[columns]).clip(min=0)
    submission = pd.DataFrame({"Id": test["Id"], "Sales": predictions})
    output = Path("submissions/submission_lgbm_baseline.csv")
    output.parent.mkdir(parents=True, exist_ok=True)
    submission.to_csv(output, index=False)
    print(f"Submission written to {output}")


if __name__ == "__main__":
    main()
