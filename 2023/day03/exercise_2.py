#!/usr/bin/env python

from dataclasses import dataclass, field
from pathlib import Path
from re import finditer
from typing import Iterable, Tuple


@dataclass
class Gear:
    start: int
    end: int
    y: int
    value: int

    def update_markers(self, markers: Iterable["Marker"]) -> None:
        checks = [
            lambda m: m.y in [self.y - 1, self.y, self.y + 1],
            lambda m: m.x >= self.start - 1 and m.x <= self.end,
        ]
        for marker in markers:
            if all([c(marker) for c in checks]):
                marker.gears.append(self)


@dataclass
class Marker:
    x: int
    y: int
    gears: list[Gear] = field(default_factory=list)

    def ratio(self) -> float:
        return self.gears[0].value * self.gears[1].value


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def parse_markers(line: str, y: int) -> Iterable[Marker]:
    for match in finditer(r"\*", line):
        loc = match.regs[0]
        yield Marker(loc[0], y)


def parse_gears(line: str, y: int) -> Iterable[Gear]:
    for match in finditer(r"\d+", line):
        loc = match.regs[0]
        yield Gear(loc[0], loc[1], y, int(match.group(0)))


def parse_input(filepath: Path) -> Tuple[Iterable[Marker], Iterable[Gear]]:
    markers = []
    gears = []
    for y, line in enumerate(parse_lines(filepath)):
        markers.extend(parse_markers(line, y))
        gears.extend(parse_gears(line, y))

    return markers, gears


def main(filepath: Path):
    markers, gears = parse_input(filepath)

    for gear in gears:
        gear.update_markers(markers)

    total = 0
    for marker in markers:
        if len(marker.gears) == 2:
            # print(marker.gears)
            total += marker.ratio()
        elif len(marker.gears) > 2:
            raise ValueError("More than 2 gears in a marker")

    print(total)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
