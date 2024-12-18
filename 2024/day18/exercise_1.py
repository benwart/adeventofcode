#!/usr/bin/env python

from dataclasses import dataclass
from math import hypot
from pathlib import Path
from typing import Iterable

from astar import find_path


@dataclass(frozen=True)
class Coord:
    x: int
    y: int


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def parse_coords(filepath: Path) -> Iterable[Coord]:
    for line in parse_lines(filepath):
        yield Coord(*map(int, line.strip().split(",")))


def print_grid(grid: list[list[str]], path: set[Coord]):
    for y, r in enumerate(grid):
        for x, c in enumerate(r):
            if Coord(x, y) in path:
                print(".", end="")
            else:
                print(c, end="")
        print("")


def main(filepath: Path, size: int, bytes: int):
    grid: list[list[str]] = [[" "] * size for _ in range(size)]
    falling: list[Coord] = [c for c in parse_coords(filepath)]

    for i in range(bytes):
        c: Coord = falling[i]
        grid[c.y][c.x] = "#"

    start: Coord = Coord(0, 0)
    end: Coord = Coord(size - 1, size - 1)

    def neighbors(c: Coord) -> Iterable[Coord]:
        for x, y in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            if c.x + x < 0 or c.x + x >= size or c.y + y < 0 or c.y + y >= size:
                continue

            if grid[c.y][c.x] == " ":
                yield Coord(c.x + x, c.y + y)

    def cost_estimate(a: Coord, b: Coord) -> bool:
        return hypot((a.x - b.x), (a.y - b.y))

    path: list[Coord] = [c for c in find_path(start, end, neighbors, heuristic_cost_estimate_fnct=cost_estimate)]

    print_grid(grid, set(path))
    print(len(path) - 1)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "example_1", 7, 12)
    main(Path(__file__).parent / "data" / "full", 71, 1024)
