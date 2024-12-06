#!/usr/bin/env python

from dataclasses import dataclass, field
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


class Result(StrEnum):
    DONE = "done"
    LOOP = "loop"
    CONTINUE = "continue"


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

    def add_obstacle(self, point: Point) -> None:
        self.grid[point.y][point.x] = Location.OBSTACLE

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

    def copy(self) -> "Map":
        c: Map = Map()
        for y in self.grid:
            c.add_line("".join(x.value for x in y))

        return c


@dataclass
class Guard:
    direction: Location
    location: Point
    map: Map
    visited: set[tuple[Point, Location]] = field(init=False, default_factory=set)

    def __post_init__(self) -> None:
        self.visited.add((self.location, self.direction))

    def points(self) -> set[Point]:
        return set([p for p, _ in self.visited])

    def walk(self) -> Result:
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
            return Result.CONTINUE

        if next_location == Location.OUTSIDE:
            return Result.DONE

        # move ahead because we aren't turning or leaving
        self.location = next_point

        # we found a loop
        if (self.location, self.direction) in self.visited:
            return Result.LOOP

        # still walking so store the visit and continue
        self.visited.add((self.location, self.direction))
        return Result.CONTINUE


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def parse_map(filepath: Path) -> Map:
    map: Map = Map()

    for line in parse_lines(filepath):
        map.add_line(line)

    return map


def walk_map(map: Map) -> tuple[Guard, Result]:
    guard: Guard = Guard(Location.GUARD_UP, map.start, map)
    result: Result = Result.CONTINUE
    while True:
        result = guard.walk()
        if result in [Result.DONE, Result.LOOP]:
            break

    return guard, result


def main(filepath: Path):
    map: Map = parse_map(filepath)

    # run through once to get all the visited locations
    guard, result = walk_map(map)

    # use the points (minus start) to place a single obstacle and search for looping patterns
    loops: int = 0
    attempts: int = 0
    for p in guard.points() - {map.start}:
        attempts += 1
        m: Map = map.copy()
        m.add_obstacle(p)

        guard, result = walk_map(m)
        if result == Result.LOOP:
            loops += 1

    print(f"Attempts: {attempts} Loops: {loops}")


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
