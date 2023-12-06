#!/usr/bin/env python

from dataclasses import dataclass
from functools import reduce
from pathlib import Path
from typing import Iterable


@dataclass
class Race:
    time: int
    distance: int


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def parse_races(filepath: Path) -> list[Race]:
    times, distances = list(parse_lines(filepath))
    times = [int(t) for t in times.split(":")[1].strip().split(" ") if t]
    distances = [int(d) for d in distances.split(":")[1].strip().split(" ") if d]

    races: list[Race] = []

    for i in range(len(times)):
        races.append(Race(times[i], distances[i]))

    return races


def calculate_winning_race_distances(race: Race) -> int:
    distances = [(t * (race.time - t)) - race.distance for t in range(1, race.time)]
    return len([d for d in distances if d > 0])


def main(filepath: Path):
    races = parse_races(filepath)
    wins = [calculate_winning_race_distances(r) for r in races]
    print(reduce(lambda x, y: x * y, wins))


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
