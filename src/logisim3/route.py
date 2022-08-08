from collections import defaultdict
from pathlib import Path
from queue import PriorityQueue

import pandas as pd
from .train_speed import SpeedModel


def route(speed_model: SpeedModel, origin: str, dest: str):

    # this is our map
    # key is the current location
    # value is a list of (location, distance)
    MAP = defaultdict(list)  # port to roads

    map_file = Path(__file__).parent / "map.csv"
    df = pd.read_csv(map_file)
    for _, r in df.iterrows():
        MAP[r.Origin].append((r.Destination, r.Distance))
        MAP[r.Destination].append((r.Origin, r.Distance))

    # list of our visited locations
    visited = []

    # priority queue to track how our truck travels through the milestones
    # it will have tuples that contain travel history as a linked list: (CLOCK, location, Parent)
    # E.g. travel history with just one milestone where truck started in city 'CITY1' will be (0, "CITY1", None)
    # If truck arrived to CITY2 at time 12, then the history will look like:
    # (12, "CITY2",
    #   (0, "CITY1", None)
    # )
    # The fun part of that is:
    # priority queue sorts by the first tuple element, so any running travels will be properly ordered.
    # we can represent multuple travels while reusing objects from the previous travels.
    # just add new miletstones and link them to the existing travel graph.
    travels = PriorityQueue()

    # this is our start location
    # travel tree will grow from here
    travels.put((0, origin, None))

    while not travels.empty():
        trip = travels.get()
        (clock, location, parent) = trip
        if location in visited:
            continue

        if location == dest:
            # we arrived. Let's reverse the trip history to print it
            path = [(clock, location)]
            while parent:
                clock, location, parent = parent
                path.append((clock, location))

            for clock, location in reversed(path):
                print(f"{clock:>5.2f}h {'ARRIVE' if clock else 'DEPART'} {location}")
            break

        visited.append(location)

        # we got work to do. Let's look through all roads that
        # lead to unvisited locations.
        for destination, distance in MAP[location]:
            if destination not in visited:
                # this destination wasn't explored, let's check it out
                # by sending a truck there
                time_of_day = int(clock % 24)
                speed = speed_model.predict(location, destination, time_of_day)
                time_to_travel = round(distance / speed, 2)
                arrival_time = clock + time_to_travel
                travels.put((arrival_time, destination, trip))
