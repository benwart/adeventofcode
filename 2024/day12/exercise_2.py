#!/usr/bin/env python

from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


@dataclass
class Plot:
    x: int
    y: int
    value: str

    def __eq__(self, other: "Plot") -> bool:
        return self.x == other.x and self.y == other.y and self.value == other.value

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.value))

    def __repr__(self) -> str:
        return f"Plot({str(self)})"

    def __str__(self) -> str:
        return f"{self.value} -> {self.x},{self.y}"


@dataclass
class Region:
    id: int
    value: str
    plots: set[Plot] = field(init=False, default_factory=set)
    fences: int = field(init=False, default=0)

    def add_plot(self, plot: Plot) -> None:
        if plot not in self.plots:
            self.plots.add(plot)

    def contains_any(self, plots: set[Plot]) -> bool:
        return len(plots.intersection(self.plots)) > 0

    def price(self) -> int:
        return len(self.plots) * self.fences

    def __repr__(self) -> str:
        return f"Region({str(self)})"

    def __str__(self) -> str:
        return f"{self.id}: {self.value} / {len(self.plots)} * {self.fences} = ${self.price()}"


@dataclass
class Map:
    grid: list[list[Plot]] = field(init=False, default_factory=list)

    def add_row(self, row: str) -> None:
        y: int = len(self.grid)
        self.grid.append([Plot(x, y, p) for x, p in enumerate(row)])

    def at(self, x: int, y: int) -> Plot:
        if 0 > x or x >= len(self.grid[0]):
            return Plot(x, y, "")

        if 0 > y or y >= len(self.grid):
            return Plot(x, y, "")

        return self.grid[y][x]


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def expand_region(m: Map, r: Region, start: Plot) -> None:
    plots: deque[Plot] = deque([start])
    seen: set[Plot] = set()

    while len(plots) > 0:
        plot: Plot = plots.popleft()
        neighbors: set[Plot] = [m.at(plot.x - 1, plot.y), m.at(plot.x, plot.y - 1), m.at(plot.x + 1, plot.y), m.at(plot.x, plot.y + 1)]
        matching: set[Plot] = {n for n in neighbors if n.value == plot.value}

        # if self or matching in region add plot
        if plot.value == r.value or r.contains_any({plot}) or r.contains_any(matching):
            r.add_plot(plot)

        # add matching that aren't already in the region
        matching.difference_update(r.plots)
        for n in matching:
            if n in seen:
                continue
            seen.add(n)
            plots.append(n)


def expand_verticle_side(m: Map, p: Plot) -> tuple[Plot, Plot]:
    t: Plot = p
    b: Plot = p

    while True:
        up: Plot = m.at(t.x, t.y - 1)
        if up.value == p.value:
            t = up
        else:
            break

    while True:
        down: Plot = m.at(b.x, b.y + 1)
        if down.value == p.value:
            b = down
        else:
            break

    return (t, b)


def expand_horizontal_side(m: Map, p: Plot) -> tuple[Plot, Plot]:
    l: Plot = p
    r: Plot = p

    while True:
        left: Plot = m.at(l.x - 1, l.y)
        if left.value == p.value:
            l = left
        else:
            break

    while True:
        right: Plot = m.at(r.x + 1, r.y)
        if right.value == p.value:
            r = right
        else:
            break

    return (l, r)


def count_sides(m: Map, r: Region) -> int:
    # find outside left edge
    p: Plot = min([p for p in r.plots if p.x == min([p for p in r.plots], key=lambda p: p.x)], key=lambda p: p.y)
    direction: str = "UP"
    sides: set[tuple[str, Plot, Plot]] = set()
    side: tuple[str, Plot, Plot]

    while True:
        match direction:
            case "UP":
                ends = expand_verticle_side(m, p)
                side = (direction, *ends)
                p = ends[0]
                direction = "RIGHT"
            case "RIGHT":
                ends = expand_horizontal_side(m, p)
                side = (direction, *ends)
                p = ends[1]
                direction = "DOWN"
            case "DOWN":
                ends = expand_verticle_side(m, p)
                side = (direction, *ends)
                p = ends[1]
                direction = "LEFT"
            case "LEFT":
                ends = expand_horizontal_side(m, p)
                side = (direction, *ends)
                p = ends[0]
                direction = "UP"

        if side not in sides:
            sides.add(side)
        else:
            break

    return len(sides)


def find_regions(m: Map) -> list[Region]:
    regions: list[Region] = []
    for row in m.grid:
        for plot in row:
            neighbors: set[Plot] = [m.at(plot.x - 1, plot.y), m.at(plot.x, plot.y - 1), m.at(plot.x + 1, plot.y), m.at(plot.x, plot.y + 1)]
            matching: set[Plot] = {n for n in neighbors if n.value == plot.value}

            region: Region
            found_region: bool = False
            if len(matching) > 0:
                # check for existing region based on matching neighbors
                for region in regions:
                    if region.value == plot.value and region.contains_any(matching):
                        found_region = True
                        break

            if not found_region:
                # no matching neighbors so this is likely a plot of 1
                region = Region(len(regions), plot.value)
                regions.append(region)

            # since we either found or added a region
            expand_region(m, region, plot)

    return regions


def main(filepath: Path):
    m: Map = Map()
    for line in parse_lines(filepath):
        m.add_row(line)

    regions: list[Region] = find_regions(m)
    for region in regions:
        region.fences = count_sides(m, region)

    total: int = sum([r.price() for r in regions])

    print(total)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "example_1")
