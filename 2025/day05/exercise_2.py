#!/usr/bin/env python

from dataclasses import dataclass, field
from itertools import combinations
from pathlib import Path
from typing import Iterable


@dataclass
class FreshRange:
    data: str
    min: int = field(init=False)
    max: int = field(init=False)

    def __post_init__(self) -> None:
        self.min, self.max = [int(d) for d in self.data.split("-")]

    def __hash__(self) -> int:
        return hash(self.data)

    def fresh(self, id: int) -> bool:
        return id >= self.min and id <= self.max

    def count(self) -> int:
        return self.max - self.min + 1

    def overlap(self, other: "FreshRange") -> bool:
        return self.fresh(other.min) or self.fresh(other.max)

    def merge(self, other: "FreshRange") -> "FreshRange":
        left: int = min(self.min, other.min)
        right: int = max(self.max, other.max)
        return FreshRange(f"{left}-{right}")


def parse_lines(lines: str) -> Iterable[str]:
    for line in lines.split("\n"):
        yield line.strip()


def parse_ranges(lines: str) -> list[FreshRange]:
    output: list[FreshRange] = []

    for line in parse_lines(lines):
        output.append(FreshRange(data=line))

    return output


def parse_ingredients(lines: str) -> list[int]:
    return [int(line) for line in parse_lines(lines) if len(line) > 0]


def parse_input(filepath: Path) -> tuple[list[FreshRange], list[int]]:
    with open(filepath, "r") as f:
        ranges, ingredients = f.read().split("\n\n")

    return parse_ranges(ranges), parse_ingredients(ingredients)


def main(filepath: Path):
    ranges, ingredients = parse_input(filepath)
    fresh: set[FreshRange] = set()

    for ingredient in ingredients:
        for range in ranges:
            if range.fresh(ingredient):
                fresh.add(range)

    merged: bool = True
    while merged:
        merged = False
        for a, b in combinations(fresh, 2):
            if a.overlap(b) or b.overlap(a):
                fresh.remove(a)
                fresh.remove(b)
                fresh.add(a.merge(b))
                merged = True
                break

    total: int = sum([r.count() for r in fresh])
    print(fresh)
    print(total)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
