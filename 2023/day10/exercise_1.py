#!/usr/bin/env python

from collections import namedtuple
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Iterable

Point = namedtuple("Point", ["y", "x"])


class Direction(StrEnum):
    NORTH = "N"
    SOUTH = "S"
    EAST = "E"
    WEST = "W"


class PipeSymbol(StrEnum):
    NORTH_SOUTH = "|"
    EAST_WEST = "-"
    NORTH_EAST = "L"
    NORTH_WEST = "J"
    SOUTH_WEST = "7"
    SOUTH_EAST = "F"
    EMPTY = "."
    START = "S"


COMPATIBLE_PIPES = {
    (PipeSymbol.START, Direction.NORTH): {
        PipeSymbol.NORTH_SOUTH,
        PipeSymbol.SOUTH_EAST,
        PipeSymbol.SOUTH_WEST,
    },
    (PipeSymbol.START, Direction.SOUTH): {
        PipeSymbol.NORTH_SOUTH,
        PipeSymbol.NORTH_EAST,
        PipeSymbol.NORTH_WEST,
    },
    (PipeSymbol.START, Direction.EAST): {
        PipeSymbol.EAST_WEST,
        PipeSymbol.NORTH_WEST,
        PipeSymbol.SOUTH_WEST,
    },
    (PipeSymbol.START, Direction.WEST): {
        PipeSymbol.EAST_WEST,
        PipeSymbol.NORTH_EAST,
        PipeSymbol.SOUTH_EAST,
    },
    (PipeSymbol.NORTH_SOUTH, Direction.NORTH): {
        PipeSymbol.NORTH_SOUTH,
        PipeSymbol.SOUTH_EAST,
        PipeSymbol.SOUTH_WEST,
        PipeSymbol.START,
    },
    (PipeSymbol.NORTH_SOUTH, Direction.SOUTH): {
        PipeSymbol.NORTH_SOUTH,
        PipeSymbol.NORTH_EAST,
        PipeSymbol.NORTH_WEST,
        PipeSymbol.START,
    },
    (PipeSymbol.EAST_WEST, Direction.EAST): {
        PipeSymbol.EAST_WEST,
        PipeSymbol.NORTH_WEST,
        PipeSymbol.SOUTH_WEST,
        PipeSymbol.START,
    },
    (PipeSymbol.EAST_WEST, Direction.WEST): {
        PipeSymbol.EAST_WEST,
        PipeSymbol.NORTH_EAST,
        PipeSymbol.SOUTH_EAST,
        PipeSymbol.START,
    },
    (PipeSymbol.NORTH_EAST, Direction.NORTH): {
        PipeSymbol.NORTH_SOUTH,
        PipeSymbol.SOUTH_EAST,
        PipeSymbol.SOUTH_WEST,
        PipeSymbol.START,
    },
    (PipeSymbol.NORTH_EAST, Direction.EAST): {
        PipeSymbol.EAST_WEST,
        PipeSymbol.NORTH_WEST,
        PipeSymbol.SOUTH_WEST,
        PipeSymbol.START,
    },
    (PipeSymbol.NORTH_WEST, Direction.NORTH): {
        PipeSymbol.NORTH_SOUTH,
        PipeSymbol.SOUTH_EAST,
        PipeSymbol.SOUTH_WEST,
        PipeSymbol.START,
    },
    (PipeSymbol.NORTH_WEST, Direction.WEST): {
        PipeSymbol.EAST_WEST,
        PipeSymbol.NORTH_EAST,
        PipeSymbol.SOUTH_EAST,
        PipeSymbol.START,
    },
    (PipeSymbol.SOUTH_WEST, Direction.SOUTH): {
        PipeSymbol.NORTH_SOUTH,
        PipeSymbol.NORTH_EAST,
        PipeSymbol.NORTH_WEST,
        PipeSymbol.START,
    },
    (PipeSymbol.SOUTH_WEST, Direction.WEST): {
        PipeSymbol.EAST_WEST,
        PipeSymbol.NORTH_EAST,
        PipeSymbol.SOUTH_EAST,
        PipeSymbol.START,
    },
    (PipeSymbol.SOUTH_EAST, Direction.SOUTH): {
        PipeSymbol.NORTH_SOUTH,
        PipeSymbol.NORTH_EAST,
        PipeSymbol.NORTH_WEST,
        PipeSymbol.START,
    },
    (PipeSymbol.SOUTH_EAST, Direction.EAST): {
        PipeSymbol.EAST_WEST,
        PipeSymbol.NORTH_WEST,
        PipeSymbol.SOUTH_WEST,
        PipeSymbol.START,
    },
}


@dataclass
class Map:
    grid: list[list[PipeSymbol]]
    start: Point
    width: int = field(init=False)
    height: int = field(init=False)

    def __post_init__(self):
        self.width = len(self.grid[0])
        self.height = len(self.grid)

    def __str__(self):
        return "\n".join("".join([c.value for c in row]) for row in self.grid)


@dataclass
class Edge:
    start: Point
    end: Point
    direction: Direction = field(init=False)

    def __post_init__(self):
        up_down = self.start.x == self.end.x
        left_right = self.start.y == self.end.y

        if up_down:
            self.direction = (
                Direction.NORTH if self.start.y > self.end.y else Direction.SOUTH
            )
        elif left_right:
            self.direction = (
                Direction.WEST if self.start.x > self.end.x else Direction.EAST
            )


def compatible(current_value, direction, point_value) -> bool:
    key = (current_value, direction)
    if key in COMPATIBLE_PIPES:
        compatible = COMPATIBLE_PIPES[key]
        if point_value in compatible:
            return True
    return False


def follow_pipe_on_map(map: Map) -> list[Point]:
    pipe: set[Point] = {map.start}

    def get_value(p: Point) -> PipeSymbol:
        return map.grid[p.y][p.x]

    current = map.start
    done = False

    while not done:
        current_value = get_value(current)

        # find all surrounding pipes
        north = Point(current.y - 1, current.x) if current.y > 0 else None
        south = Point(current.y + 1, current.x) if current.y < map.height - 1 else None
        east = Point(current.y, current.x + 1) if current.x < map.width - 1 else None
        west = Point(current.y, current.x - 1) if current.x > 0 else None
        nearby = [north, south, east, west]

        # find the next segment of the pipe
        for point in nearby:
            if point and point not in pipe:
                edge = Edge(current, point)
                point_value = get_value(point)

                if compatible(current_value, edge.direction, point_value):
                    pipe.add(point)
                    current = point
                    break

        # if we didn't find a new segment, we're done
        else:
            done = True

    return pipe


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def parse_map(filepath: Path) -> Map:
    grid: list[list[str]] = []
    start: Point = None

    for y, line in enumerate(parse_lines(filepath)):
        row = [PipeSymbol(c) for c in line]
        grid.append(row)

        if PipeSymbol.START in row:
            start = Point(y, row.index(PipeSymbol.START))

    return Map(grid, start)


def main(filepath: Path):
    map = parse_map(filepath)
    pipe = follow_pipe_on_map(map)
    print(f"Found {len(pipe)} pipes with middle at {len(pipe) // 2}")


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
