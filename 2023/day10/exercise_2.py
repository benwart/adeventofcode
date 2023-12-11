#!/usr/bin/env python

from collections import deque
from dataclasses import dataclass, field
from enum import StrEnum
from functools import partial
from multiprocessing import Pool
from pathlib import Path
from typing import Iterable

from shapely import Point, LinearRing, Polygon
from tqdm import tqdm as progress


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


ALTERNATE_PIPES = {
    PipeSymbol.SOUTH_EAST: "╭",
    PipeSymbol.EAST_WEST: "─",
    PipeSymbol.SOUTH_WEST: "╮",
    PipeSymbol.NORTH_SOUTH: "│",
    PipeSymbol.NORTH_WEST: "╯",
    PipeSymbol.NORTH_EAST: "╰",
    PipeSymbol.START: "█",
    PipeSymbol.EMPTY: " ",
}


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
        return "\n".join(
            "".join([ALTERNATE_PIPES[c] for c in row]) for row in self.grid
        )


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
    pipe: list[Point] = [map.start]
    pipe_set: set[Point] = set(pipe)

    def get_value(p: Point) -> PipeSymbol:
        return map.grid[int(p.y)][int(p.x)]

    current = map.start
    done = False

    while not done:
        current_value = get_value(current)

        # find all surrounding pipes
        north = Point(current.x, current.y - 1) if current.y > 0 else None
        south = Point(current.x, current.y + 1) if current.y < map.height - 1 else None
        east = Point(current.x + 1, current.y) if current.x < map.width - 1 else None
        west = Point(current.x - 1, current.y) if current.x > 0 else None
        nearby = [north, south, east, west]

        # find the next segment of the pipe
        for point in nearby:
            if point and point not in pipe_set:
                edge = Edge(current, point)
                point_value = get_value(point)

                if compatible(current_value, edge.direction, point_value):
                    pipe_set.add(point)
                    pipe.append(point)
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
            start = Point(row.index(PipeSymbol.START), y)

    return Map(grid, start)


def check_point(polygon: Polygon, p: Point) -> tuple[bool, Point]:
    contains = polygon.contains(p)
    return (contains, p)


def calculate_inside_points(map: Map, pipe: list[Point]) -> set[Point]:
    # create polygon from pipe
    polygon = Polygon(LinearRing([(p.x, p.y) for p in pipe]).coords)
    pipe_set = set(pipe)

    # find all points inside polygon
    check_points = deque()
    check_inside_polygon = partial(check_point, polygon)
    inside_points: set[Point] = set()

    for y, row in enumerate(map.grid):
        for x, _ in enumerate(row):
            p = Point(x, y)
            if p not in pipe_set:
                check_points.append(p)

    # check each point in parallel
    with Pool(10) as pool:
        for inside, point in progress(
            pool.imap(check_inside_polygon, check_points), total=len(check_points)
        ):
            if inside:
                inside_points.add(point)

    # return points inside polygon that are not in pipe
    return inside_points


def convert_point(
    pipe: set[Point], inside: set[Point], r_y: tuple[list[PipeSymbol], int]
) -> tuple[list[str], int]:
    row, y = r_y
    output_row = []
    for x, c in enumerate(row):
        p = Point(x, y)

        if p in pipe:
            output_row.append(ALTERNATE_PIPES[c])
        elif p in inside:
            output_row.append("×")
        else:
            output_row.append(" ")

    return output_row, y


def render_map(map: Map, pipe: set[Point], inside: set[Point] = []):
    converted: list[list[str]] = []

    convert_rows = deque()
    convert_point_partial = partial(convert_point, pipe, inside)
    for y, row in enumerate(map.grid):
        converted.append([c for c in ALTERNATE_PIPES[PipeSymbol.EMPTY] * len(row)])
        convert_rows.append((row, y))

    with Pool(10) as pool:
        for row, y in progress(
            pool.imap(convert_point_partial, convert_rows), total=len(convert_rows)
        ):
            for x, c in enumerate(row):
                if converted[y][x] == " ":
                    converted[y][x] = c
                else:
                    raise ValueError("Location is already set to a pipe symbol")

    return "\n".join(
        "".join([c for c in [f"{y}", *[c for c in " " * (4 - len(f"{y}"))]] + row])
        for y, row in enumerate(converted)
    )


def main(filepath: Path):
    map = parse_map(filepath)
    pipe = follow_pipe_on_map(map)

    print(f"Found {len(pipe)} pipes with middle at {len(pipe) // 2}")

    inside = calculate_inside_points(map, pipe)

    print(render_map(map, set(pipe), inside))
    print(f"Points inside pipe: {len(inside)}")


if __name__ == "__main__":
    filepath = Path("2023") / "day10" / "data" / "full"
    main(filepath)
