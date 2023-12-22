#!/usr/bin/env python

from colorama import Fore, Style
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Iterable


class PointChar(StrEnum):
    GARDEN = "."
    ROCK = "#"
    START = "S"
    STEP = "O"


def point_char_str(char: PointChar) -> str:
    match char:
        case PointChar.GARDEN:
            return f"{Style.DIM}{Fore.WHITE}{char.value}{Style.RESET_ALL}"
        case PointChar.ROCK:
            return f"{Style.DIM}{Fore.BLACK}{char.value}{Style.RESET_ALL}"
        case PointChar.START:
            return f"{Style.BRIGHT}{Fore.WHITE}{char.value}{Style.RESET_ALL}"
        case PointChar.STEP:
            return f"{Style.BRIGHT}{Fore.BLUE}{char.value}{Style.RESET_ALL}"


@dataclass
class Point:
    x: int
    y: int

    def __str__(self) -> str:
        return f"({self.x},{self.y})"

    def __hash__(self) -> int:
        return hash((self.x, self.y))


@dataclass
class Map:
    grid: list[list[PointChar]]

    def neighbors(self, point: Point) -> set[Point]:
        neighbors = set()

        possible = [
            Point(point.x - 1, point.y),
            Point(point.x + 1, point.y),
            Point(point.x, point.y - 1),
            Point(point.x, point.y + 1),
        ]

        for p in possible:
            if p.x < 0 or p.y < 0 or p.x >= len(self.grid[0]) or p.y >= len(self.grid):
                continue

            if self.grid[p.y][p.x] == PointChar.GARDEN:
                neighbors.add(p)

        return neighbors


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def parse_map(lines: Iterable[str]) -> tuple[Map, set[Point]]:
    grid: list[list[PointChar]] = []
    start = set()
    for y, line in enumerate(lines):
        row: list[PointChar] = []
        for x, c in enumerate(line):
            if c == PointChar.START:
                row.append(PointChar.GARDEN)
                start.add(Point(x, y))
            else:
                row.append(PointChar(c))

        grid.append(row)

    return Map(grid), start


def plot_map(map: Map, step: set[Point]) -> None:
    for y, row in enumerate(map.grid):
        for x, c in enumerate(row):
            if Point(x, y) in step:
                print(point_char_str(PointChar.STEP), end="")
            else:
                print(point_char_str(c), end="")
        print()


def next_step(map: Map, starting: set[Point]) -> set[Point]:
    next = set()
    for p in starting:
        next |= map.neighbors(p)

    return next


def main(filepath: Path):
    map, start = parse_map(parse_lines(filepath))

    for i in range(64):
        # print(f"\nStep {i+1}")
        step = next_step(map, start)
        # plot_map(map, step)
        start = step

    print("\nTotal:", len(start))


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
