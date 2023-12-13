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


def mirrors(grid: list[str], width: int, height: int) -> Optional[list[int]]:
    pairs = []

    for bi in range(1, height):
        ti = bi - 1
        top = grid[ti]
        bottom = grid[bi]

        if top == bottom:
            pairs.append((ti, bi))

    match = False

    for ai, bi in pairs:
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

            if top != bottom:
                match = False
                break

        if match:
            return bi

    return None


def main(filepath: Path):
    total = 0
    for map in parse_maps(filepath):
        # print("--------------------------------")
        # print(map)
        mirror = 0
        v = mirrors(map.grid, map.width, map.height)
        if v:
            mirror = v * 100
        else:
            h = mirrors(transpose(map.grid), map.height, map.width)
            if h:
                mirror = h
            else:
                print("No mirror found")

        total += mirror

    print(f"Total: {total}")


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
