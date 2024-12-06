#!/usr/bin/env python

from dataclasses import InitVar, dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Iterable


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self) -> int:
        return hash((self.x, self.y))


class Location(StrEnum):
    GUARD_UP = "^"
    GUARD_LEFT = "<"
    GUARD_RIGHT = ">"
    GUARD_DOWN = "v"
    OBSTACLE = "#"
    OPEN = "."
    OUTSIDE = "x"


@dataclass
class Map:
    grid: list[list[Location]] = field(init=False, default_factory=list)
    start: Point = field(init=False, default_factory=lambda: Point(0, 0))

    def add_line(self, line: str) -> None:
        self.grid.append([Location(c) for c in line])

        # check for start location
        if Location.GUARD_UP in line:
            x = line.index(Location.GUARD_UP)
            y = len(self.grid) - 1
            self.start = Point(x, y)

    def at(self, point: Point) -> Location:
        # if we are outside the map return outside
        if (point.y > len(self.grid) - 1) or (point.y < 0):
            return Location.OUTSIDE

        if (point.x > len(self.grid[0]) - 1) or (point.x < 0):
            return Location.OUTSIDE

        # if we are inside the map return the location
        return self.grid[point.y][point.x]

    def print(self) -> None:
        print(f"Start: {self.start}")
        for line in self.grid:
            print("".join(c.value for c in line))


@dataclass
class Guard:
    direction: Location
    location: Point
    map: Map
    visited: set[Point] = field(init=False, default_factory=set)

    def __post_init__(self) -> None:
        self.visited.add(self.location)

    def walk(self) -> bool:
        # walk 1 step forward and return true if we are still in the map
        next_point: Point
        match self.direction:
            case Location.GUARD_UP:
                next_point = Point(self.location.x, self.location.y - 1)
            case Location.GUARD_DOWN:
                next_point = Point(self.location.x, self.location.y + 1)
            case Location.GUARD_LEFT:
                next_point = Point(self.location.x - 1, self.location.y)
            case Location.GUARD_RIGHT:
                next_point = Point(self.location.x + 1, self.location.y)

        next_location: Location = self.map.at(next_point)

        if next_location == Location.OBSTACLE:
            # turn 90 degrees
            match self.direction:
                case Location.GUARD_UP:
                    self.direction = Location.GUARD_RIGHT
                case Location.GUARD_DOWN:
                    self.direction = Location.GUARD_LEFT
                case Location.GUARD_LEFT:
                    self.direction = Location.GUARD_UP
                case Location.GUARD_RIGHT:
                    self.direction = Location.GUARD_DOWN

            # don't go ahead if we do a rotation
            return True

        if next_location == Location.OUTSIDE:
            return False

        # move ahead because we aren't turning or leaving
        self.location = next_point
        self.visited.add(self.location)

        return True


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def main(filepath: Path):
    map: Map = Map()

    for line in parse_lines(filepath):
        map.add_line(line)

    guard: Guard = Guard(Location.GUARD_UP, map.start, map)

    while guard.walk():
        pass

    print(len(guard.visited))


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
