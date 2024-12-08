#!/usr/bin/env python

from dataclasses import dataclass, field
from itertools import permutations
from pathlib import Path
from typing import Iterable


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self) -> int:
        return hash(
            (
                self.x,
                self.y,
            )
        )


@dataclass
class Grid:
    rows: list[str] = field(init=False, default_factory=list)
    frequencies: dict[set, list[Point]] = field(init=False, default_factory=dict)
    antinodes: set[Point] = field(init=False, default_factory=set)

    def at(self, x: int, y: int) -> str:
        return self.rows[y][x]

    def inside(self, point: Point) -> bool:
        return 0 <= point.x < len(self.rows[0]) and 0 <= point.y < len(self.rows)


def add_line(grid: Grid, line: str) -> None:
    # initialize the variables
    y: int = len(grid.rows)
    x: int

    # add the frequencies
    for x, c in enumerate(line):
        if c != ".":
            if c not in grid.frequencies:
                grid.frequencies[c] = []
            grid.frequencies[c].append(Point(x, y))

    # add the row to the rows
    grid.rows.append(line)


def compute_antinodes(grid: Grid) -> None:
    for f, points in grid.frequencies.items():
        if points == 1:
            continue

        # for each pair of points generate an antinode
        # the iterator will geneate both a,b and b,a for each pair
        for a, b in permutations(points, r=2):
            delta: Point = Point(a.x - b.x, a.y - b.y)
            antinode: Point = Point(a.x + delta.x, a.y + delta.y)

            # make sure the antinode is inside the grid
            if grid.inside(antinode):
                grid.antinodes.add(antinode)


def print_base(grid: Grid) -> None:
    for row in grid.rows:
        print(row)


def print_antinodes(grid: Grid) -> None:
    for y, row in enumerate(grid.rows):
        line: list[str] = []
        for x, _ in enumerate(row):
            if Point(x, y) in grid.antinodes:
                line.append("#")
            else:
                line.append(".")
        print("".join(line))


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def main(filepath: Path):
    grid: Grid = Grid()
    for line in parse_lines(filepath):
        add_line(grid, line)

    compute_antinodes(grid)
    print(f"\n{len(grid.antinodes)}")


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
