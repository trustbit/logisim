from pathlib import Path
import pandas as pd
import numpy as np


class SpeedModel:
    def __init__(self, segments: dict):
        self.segments = segments

    def predict(self, orig: str, dest: str, hour: int) -> float:
        model = self.segments[(orig, dest)]
        prediction = model(hour)
        return prediction


def train(test_ratio=0.2) -> SpeedModel:
    history_file = Path(__file__).parent / "history.csv"

    df = pd.read_csv(history_file, parse_dates=["Time"])
    df["Hour"] = df.apply(lambda x: x.Time.time().hour, axis=1)

    # get random sample
    test_df = df.sample(frac=test_ratio, axis=0, random_state=1)
    # get everything but the test sample
    train_df = df.drop(index=test_df.index)

    # we are going to have a model per road segment
    models = {}
    # group data for each segment together
    for k, grp in train_df.groupby(["Origin", "Destination"]):
        # fit polynomial regression
        model = np.poly1d(np.polyfit(grp.Hour, grp.Speed, 3))
        models[k] = model

    model = SpeedModel(models)

    test_df["Predict"] = test_df.apply(
        lambda x: model.predict(x.Origin, x.Destination, x.Hour), axis=1
    )

    MSE = ((test_df.Predict - test_df.Speed) ** 2).mean()

    print(f"Mean squared error is {MSE:.4f}")

    return model
