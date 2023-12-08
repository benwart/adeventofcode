#!/usr/bin/env python

from dataclasses import dataclass, field
from enum import StrEnum
from math import gcd
from pathlib import Path
from re import match
from typing import Iterable


class Direction(StrEnum):
    LEFT = "L"
    RIGHT = "R"


@dataclass
class Location:
    id: str
    left: str
    right: str
    stop: bool = field(init=False)

    def __post_init__(self):
        self.stop = self.id.endswith("Z")


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def parse_directions(directions: str) -> Iterable[Direction]:
    for d in directions:
        yield Direction(d)


def parse_locations(parser: Iterable[str]) -> Iterable[Location]:
    for line in parser:
        if line:
            m = match(r"(?P<id>\w+) = \((?P<left>\w+), (?P<right>\w+)\)", line)
            if m:
                g = m.groupdict()
                yield Location(g["id"], g["left"], g["right"])


def main(filepath: Path):
    parser = parse_lines(filepath)
    directions = list(parse_directions(next(parser)))
    # print(directions)

    locations = {loc.id: loc for loc in parse_locations(parser)}

    starts: list[Location] = []

    for location in locations.values():
        if location.id.endswith("A"):
            starts.append(location)

    stops: list[int] = []

    for start in starts:
        print(f"Starting from {start.id}", end="")
        current = start
        steps = 0
        not_found = True

        # find the steps for each start to stop
        while not_found:
            for d in directions:
                current = locations[getattr(current, d.name.lower())]
                steps += 1
                if current.stop:
                    print(f" - {steps}")
                    not_found = False
                    stops.append(steps)
                    break

    # least common multiple for all steps to stop
    # as running this out will take too long
    lcm = 1
    for i in stops:
        lcm = lcm * i // gcd(lcm, i)

    print(f"Least common multiple: {lcm}")


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
