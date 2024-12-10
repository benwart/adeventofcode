#!/usr/bin/env python

from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Deque, Iterable


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self) -> int:
        return hash(repr(self))

    def __repr__(self) -> str:
        return f"Point({str(self)})"

    def __str__(self) -> str:
        return f"{self.x},{self.y}"


@dataclass
class Trail:
    route: list[Point]

    def copy(self) -> "Trail":
        return Trail(self.route.copy())

    def start(self) -> Point:
        return self.route[0]

    def end(self) -> Point:
        return self.route[-1]

    def add_point(self, point: Point) -> None:
        self.route.append(point)

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self) -> int:
        return hash(repr(self))

    def __repr__(self) -> str:
        return f"Trail({str(self)})"

    def __str__(self) -> str:
        return f"{self.start()}, {self.end()}"


@dataclass
class Grid:
    rows: list[list[int]] = field(init=False, default_factory=list)
    starts: list[Point] = field(init=False, default_factory=list)

    def append_line(self, line: list[int]) -> None:
        y: int = len(self.rows)
        self.rows.append(line)
        starts: list[Point] = [Point(i, y) for i, v in enumerate(line) if v == 0]
        self.starts.extend(starts)

    def at(self, coords: Point) -> int:
        return self.rows[coords.y][coords.x]


def parse_lines(filepath: Path) -> Iterable[list[int]]:
    with open(filepath, "r") as f:
        for line in f:
            yield list(map(int, line.strip()))


def walk(grid: Grid, trail: Trail) -> list[Trail]:
    directions: list[Point] = [
        Point(1, 0),  # right
        Point(-1, 0),  # left
        Point(0, 1),  # down
        Point(0, -1),  # up
    ]
    trails: list[Trail] = []
    # walk a step on the trail in all directions
    for d in directions:
        # figure out the points to compare
        ep: Point = trail.end()

        nx: int = ep.x + d.x
        ny: int = ep.y + d.y

        if nx < 0 or nx >= len(grid.rows[0]):
            continue

        if ny < 0 or ny >= len(grid.rows):
            continue

        np: Point = Point(ep.x + d.x, ep.y + d.y)

        # get the grid value
        epv: int = grid.at(ep)
        npv: int = grid.at(np)

        # create a new trail for each direction that is valid
        if (epv + 1) == npv:
            nt: Trail = trail.copy()
            nt.add_point(np)
            trails.append(nt)

    # return all trails that are still valid
    return trails


def main(filepath: Path):
    grid: Grid = Grid()
    for line in parse_lines(filepath):
        grid.append_line(line)

    trails: deque[Trail] = deque()

    # initialize the trails
    start: Point
    for start in grid.starts:
        trails.append(Trail([start]))

    # follow the trails
    final: deque[Trail] = deque()
    while trails:
        trail: Trail = trails.popleft()

        # check if the trail is complete
        if grid.at(trail.end()) == 9:
            final.append(trail)
            continue

        # walk the trail getting all new trails
        nt: list[Trail] = walk(grid, trail)
        trails.extend(nt)

    # count all the trails
    print(len(final))


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
