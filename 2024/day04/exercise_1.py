#!/usr/bin/env python

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

SEARCH_WORD: str = "XMAS"


@dataclass
class Coord:
    x: int
    y: int


@dataclass
class Grid:
    rows: list[str] = field(init=False, default_factory=list)

    def add_row(self, row: str) -> list[Coord]:
        self.rows.append(row)
        y = len(self.rows) - 1
        return [Coord(x, y) for x, c in enumerate(row) if c == SEARCH_WORD[0]]

    def value(self, x: int, y: int) -> str:
        if 0 > x or x >= len(self.rows[0]):
            return ""

        if 0 > y or y >= len(self.rows):
            return ""

        return self.rows[y][x]


@dataclass
class Puzzle:
    grid: Grid = field(init=False, default_factory=Grid)

    def add_row(self, row: str) -> list[Coord]:
        return self.grid.add_row(row)

    def value(self, coord: Coord) -> str:
        return self.grid.value(coord.x, coord.y)

    def offset(self, coord: Coord, x: int, y: int) -> str:
        return self.grid.value(coord.x + x, coord.y + y)


def follow(puzzle: Puzzle, start: Coord, x: int, y: int) -> str:
    l: Coord = start
    word: list[str] = []
    for c in SEARCH_WORD:
        word.append(puzzle.value(l))
        l = Coord(l.x + x, l.y + y)

    return "".join(word)


def check(puzzle: Puzzle, start: Coord) -> int:
    directions: list[tuple[int, int]] = [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 0),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    ]

    found: int = 0

    for f in directions:
        if follow(puzzle, start, f[0], f[1]) == SEARCH_WORD:
            found += 1

    return found


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def main(filepath: Path):
    # keep track of starting locations
    starts: list[Coord] = []

    # setup puzzle
    puzzle: Puzzle = Puzzle()
    for line in parse_lines(filepath):
        starts.extend(puzzle.add_row(line))

    # check each starting location for xmas
    found: int = 0
    for start in starts:
        found += check(puzzle, start)

    print(found)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
