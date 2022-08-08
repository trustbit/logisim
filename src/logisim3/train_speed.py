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


DIR = Path(__file__).parent


def segment(r) -> str:
    if r.Orig < r.Dest:
        return f"{r.Orig}-{r.Dest}"
    else:
        return f"{r.Dest}-{r.Orig}"


def departure(r) -> float:
    arrival = r.Time
    travel = r.Km / r.Speed

    departure = (arrival - pd.Timedelta(hours=travel)).time()
    hour = departure.hour + departure.minute / 60.0
    return hour


def train(test_ratio=0.2) -> SpeedModel:
    df = pd.read_csv(DIR / "history.csv", parse_dates=["Time"])
    df["Segment"] = df.apply(segment, axis=1)
    map_df = pd.read_csv(DIR / "map.csv")
    map_df["Segment"] = map_df.apply(segment, axis=1)

    df = df.merge(
        map_df[["Segment", "Km"]], left_on=["Segment"], right_on=["Segment"], how="left"
    )

    df["Depart"] = df.apply(departure, axis=1)
    print(df)

    # get random sample
    test_df = df.sample(frac=test_ratio, axis=0, random_state=1)
    # get everything but the test sample
    train_df = df.drop(index=test_df.index)

    # we are going to have a model per road segment
    models = {}
    # group data for each segment together
    for k, grp in train_df.groupby(["Orig", "Dest"]):
        # fit polynomial regression
        model = np.poly1d(np.polyfit(grp.Depart, grp.Speed, 3))
        models[k] = model

    model = SpeedModel(models)

    test_df["Predict"] = test_df.apply(
        lambda x: model.predict(x.Orig, x.Dest, x.Depart), axis=1
    )

    MSE = ((test_df.Predict - test_df.Speed) ** 2).mean()

    print(f"Mean squared error is {MSE:.4f}")

    return model
