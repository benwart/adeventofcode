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


def horizontal_mirrors(map: Map) -> Optional[list[int]]:
    pairs = []

    for ri in range(1, map.width):
        li = ri - 1
        left = "".join(map.grid[y][li] for y in range(map.height))
        right = "".join(map.grid[y][ri] for y in range(map.height))

        if left == right:
            pairs.append((li, ri))

    match = False

    for ai, bi in pairs:
        match = True
        li = ai
        ri = bi

        while match:
            li -= 1
            ri += 1

            if li < 0 or ri >= map.width:
                break

            left = "".join(map.grid[y][li] for y in range(map.height))
            right = "".join(map.grid[y][ri] for y in range(map.height))

            if left != right:
                match = False
                break

        if match:
            return bi

    return None


def vertical_mirrors(map: Map) -> Optional[list[int]]:
    pairs = []

    for bi in range(1, map.height):
        ti = bi - 1
        top = map.grid[ti]
        bottom = map.grid[bi]

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

            if ti < 0 or bti >= map.height:
                break

            top = map.grid[ti]
            bottom = map.grid[bti]

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
        h = horizontal_mirrors(map)
        if h:
            mirror = h
            # print(f"Horizontal mirror: {h} found")
        else:
            v = vertical_mirrors(map)
            if v:
                mirror = v * 100
                # print(f"Vertical mirror: {v} found")
            else:
                print("No mirror found")

        total += mirror

    print(f"Total: {total}")


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
