#!/usr/bin/env python

from dataclasses import dataclass, field, InitVar
from pathlib import Path
from typing import Iterable


@dataclass
class Location:
    x: int
    y: int
    value: str


@dataclass
class Grid:
    input: InitVar[Iterable[str]]
    data: list[list[Location]] = field(init=False, default_factory=list)

    def at(self, x: int, y: int) -> Location:
        if (x < 0 or x >= self.cols) or (y < 0 or y >= self.rows):
            return Location(x, y, ".")

        return self.data[y][x]

    def is_accessible(self, x: int, y: int) -> bool:
        loc: Location = self.at(x, y)

        if loc.value != "@":
            return False

        adjancent: list[str] = [
            self.at(x - 1, y - 1).value,
            self.at(x, y - 1).value,
            self.at(x + 1, y - 1).value,
            self.at(x - 1, y).value,
            self.at(x + 1, y).value,
            self.at(x - 1, y + 1).value,
            self.at(x, y + 1).value,
            self.at(x + 1, y + 1).value,
        ]

        return len([a for a in adjancent if a == "@"]) < 4

    @property
    def rows(self) -> int:
        return len(self.data)

    @property
    def cols(self) -> int:
        return len(self.data[0])

    def __post_init__(self, input: Iterable[str]) -> None:
        for y, row in enumerate(input):
            data: list[Location] = []
            for x, value in enumerate(row):
                data.append(Location(x, y, value))

            self.data.append(data)

    def __repr__(self) -> str:
        rendered: list[str] = []
        for y in self.data:
            rendered.append("".join([x.value for x in y]))
        return "\n".join(rendered)


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def main(filepath: Path):
    grid: Grid = Grid([line for line in parse_lines(filepath)])
    print(grid)

    total: int = 0
    removed: list[Location] = []

    while True:
        removed = []
        for y in range(grid.rows):
            for x in range(grid.cols):
                if grid.is_accessible(x, y):
                    total += 1
                    removed.append(grid.at(x, y))

        if len(removed) == 0:
            break

        # remove the locations
        for loc in removed:
            loc.value = "."

    print(total)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
