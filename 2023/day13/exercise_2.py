#!/usr/bin/env python

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Optional


@dataclass
class Map:
    grid: list[str]
    height: int = field(init=False)
    width: int = field(init=False)

    def __post_init__(self):
        self.height = len(self.grid)
        self.width = len(self.grid[0])

    def __str__(self):
        return "\n".join(self.grid)


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def parse_maps(filepath: Path) -> Iterable[Map]:
    grid = []
    for line in parse_lines(filepath):
        if not line:
            yield Map(grid)
            grid = []
        else:
            grid.append(line)

    yield Map(grid)


def transpose(grid: list[str]) -> list[str]:
    transposed = []
    width = len(grid[0])
    height = len(grid)

    for x in range(width):
        transposed.append("".join(grid[y][x] for y in range(height)))

    return transposed


def compare_errors(row: str, other: str, tolerance: int) -> int:
    errors = 0
    for i in range(len(row)):
        if row[i] != other[i]:
            errors += 1

    return errors


def mirrors(grid: list[str], height: int, tolerance: int = 1) -> Optional[list[int]]:
    pairs = []

    for bi in range(1, height):
        ti = bi - 1
        top = grid[ti]
        bottom = grid[bi]
        errors = compare_errors(top, bottom, tolerance)

        if errors <= tolerance:
            pairs.append((ti, bi, tolerance - errors))

    match = False

    for ai, bi, remaining in pairs:
        match = True
        ti = ai
        bti = bi

        while match:
            ti -= 1
            bti += 1

            if ti < 0 or bti >= height:
                break

            top = grid[ti]
            bottom = grid[bti]

            errors = compare_errors(top, bottom, remaining)
            remaining -= errors

            if remaining < 0:
                match = False
                break

        if match and remaining == 0:
            return bi

    return None


def main(filepath: Path):
    total = 0
    for map in parse_maps(filepath):
        # print("--------------------------------")
        # print(map)
        mirror = 0
        v = mirrors(map.grid, map.height)
        if v:
            mirror = v * 100
        else:
            h = mirrors(transpose(map.grid), map.width)
            if h:
                mirror = h
            else:
                print("No mirror found")

        total += mirror

    print(f"Total: {total}")


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
