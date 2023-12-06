#!/usr/bin/env python

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from tqdm import tqdm as progress


@dataclass
class Race:
    time: int
    distance: int


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def parse_races(filepath: Path) -> Race:
    time, distance = list(parse_lines(filepath))
    time = int(time.split(":")[1].strip().replace(" ", ""))
    distance = int(distance.split(":")[1].strip().replace(" ", ""))

    return Race(time, distance)


def calculate_winning_race_distances(race: Race) -> int:
    distances = []
    for t in progress(range(1, race.time)):
        distance = (t * (race.time - t)) - race.distance
        if distance > 0:
            distances.append(distance)

    return len(distances)


def main(filepath: Path):
    race = parse_races(filepath)
    wins = calculate_winning_race_distances(race)
    print(wins)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
