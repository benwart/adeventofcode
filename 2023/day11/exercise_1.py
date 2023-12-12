#!/usr/bin/env python

from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Iterable

from shapely import Point


@dataclass
class Image:
    map: list[list[str]]

    def __str__(self):
        return "\n".join(["".join(c for c in row) for row in self.map])

    def empty_rows(self) -> Iterable[int]:
        for y, row in enumerate(self.map):
            if "#" not in row:
                yield y

    def empty_cols(self) -> list[int]:
        for x in range(len(self.map[0])):
            col = [row[x] for row in self.map]
            if "#" not in col:
                yield x

    def expand_empty_rows(self):
        expanded = self.map
        width = len(self.map[0])

        for y in reversed(list(self.empty_rows())):
            expanded.insert(y, ["." for _ in range(width)])

    def expand_empty_cols(self):
        expanded = self.map

        for x in reversed(list(self.empty_cols())):
            for y, row in enumerate(expanded):
                row.insert(x, ".")

    def galaxies(self) -> Iterable[Point]:
        for y, row in enumerate(self.map):
            for x, c in enumerate(row):
                if c == "#":
                    yield Point(x, y)

    def galaxy_pairs(self) -> Iterable[tuple[Point, Point]]:
        galaxies = list(self.galaxies())
        for pair in combinations(galaxies, 2):
            yield pair


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def parse_image(filepath: Path):
    map: list[list[str]] = []

    for line in parse_lines(filepath):
        map.append([c for c in line])

    return Image(map)


def min_distance(a: Point, b: Point) -> int:
    delta_y = abs(a.y - b.y)
    delta_x = abs(a.x - b.x)

    return delta_x + delta_y


def main(filepath: Path):
    image = parse_image(filepath)
    # print(image)

    # empty_rows = list(image.empty_rows())
    # empty_cols = list(image.empty_cols())
    # print(empty_rows, empty_cols)

    image.expand_empty_rows()
    image.expand_empty_cols()
    print(image)

    total = 0
    for pair in image.galaxy_pairs():
        distance = min_distance(*pair)
        total += distance

    print(f"Total distance: {int(total)}")


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
