import fire

from .route import route
from .train_speed import train


def train_and_route(
    origin: str = "Steamdrift", dest: str = "Leverstorm", test_ratio=0.2
):
    """
    train speed model and then route truck.
    """

    model = train(test_ratio)
    route(model, origin, dest)


def main():
    fire.Fire(train_and_route)
