#!/usr/bin/env python

from collections import deque
from dataclasses import InitVar, dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Deque, Iterable, Optional


class PointType(StrEnum):
    PATH = "."
    FOREST = "#"
    SLOPE_UP = "^"
    SLOPE_DOWN = "v"
    SLOPE_LEFT = "<"
    SLOPE_RIGHT = ">"


class Direction(StrEnum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"


@dataclass
class Point:
    x: int
    y: int
    type: PointType

    def __eq__(self, other: "Point") -> bool:
        return self.x == other.x and self.y == other.y and self.type == other.type

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.type))

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


@dataclass
class Route:
    points: InitVar[Iterable[Point]]
    trail: list[Point] = field(init=False)
    check: set[Point] = field(default_factory=set)

    def __post_init__(self, points: Iterable[Point]) -> None:
        self.trail = list(points)
        self.check = set(points)

    def __str__(self) -> str:
        return " -> ".join(str(p) for p in self.trail)


@dataclass
class Map:
    grid: list[list[Point]]

    def __str__(self) -> str:
        return "\n".join("".join(p.type.value for p in row) for row in self.grid)

    def at(self, x: int, y: int) -> Optional[Point]:
        if y < 0 or y >= len(self.grid) or x < 0 or x >= len(self.grid[y]):
            return None

        return self.grid[y][x]

    def neighbors(self, point: Point) -> Iterable[tuple[Point, Direction]]:
        for dx, dy, d in ((0, 1, Direction.DOWN), (0, -1, Direction.UP), (1, 0, Direction.RIGHT), (-1, 0, Direction.LEFT)):
            n = self.at(point.x + dx, point.y + dy)
            if n is not None:
                yield n, d

    def paths(self, point: Point) -> Iterable[Point]:
        for n, d in self.neighbors(point):
            if n.type == PointType.PATH:
                yield n
            if n.type in (PointType.SLOPE_UP, PointType.SLOPE_DOWN, PointType.SLOPE_LEFT, PointType.SLOPE_RIGHT):
                if n.type.name.endswith(d.name):
                    yield n

    def start(self) -> Point:
        first = self.grid[0]
        for point in first:
            if point.type == PointType.PATH:
                return point

        raise ValueError("No start found")

    def end(self) -> Point:
        last = self.grid[-1]
        for point in last:
            if point.type == PointType.PATH:
                return point

        raise ValueError("No end found")


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def parse_map(lines: Iterable[str]) -> Map:
    grid = []

    for y, line in enumerate(lines):
        row = []
        for x, char in enumerate(line):
            row.append(Point(x, y, PointType(char)))

        grid.append(row)

    return Map(grid)


def main(filepath: Path):
    map = parse_map(parse_lines(filepath))
    complete: list[Route] = []
    end = map.end()

    routes: Deque[Route] = deque([Route([map.start()])])
    while len(routes):
        r = routes.popleft()
        p = r.trail[-1]

        if p == end:
            complete.append(r)
            continue

        for n in map.paths(p):
            if n not in r.check:
                routes.append(Route(r.trail + [n]))

    longest = max(complete, key=lambda r: len(r.trail))
    print(f"Longest route: {len(longest.trail)-1}")


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
