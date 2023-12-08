#!/usr/bin/env python

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from re import match
from typing import Iterable, Optional


class Direction(StrEnum):
    LEFT = "L"
    RIGHT = "R"


@dataclass
class Location:
    id: str
    left: str
    right: str
    LEFT: Optional["Location"] = None
    RIGHT: Optional["Location"] = None

    def __eq__(self, value: "Location") -> bool:
        return self.id == value.id


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
    print(directions)

    locations = {loc.id: loc for loc in parse_locations(parser)}

    for location in locations.values():
        location.LEFT = locations[location.left]
        location.RIGHT = locations[location.right]

    start = locations["AAA"]
    stop = locations["ZZZ"]
    current = start
    steps = 0

    while True:
        for d in directions:
            current = getattr(current, d.name)
            steps += 1
            if current == stop:
                print(f"Found it in {steps}")
                return


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
