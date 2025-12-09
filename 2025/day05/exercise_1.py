#!/usr/bin/env python

from dataclasses import dataclass, field, InitVar
from pathlib import Path
from typing import Iterable


@dataclass
class FreshRange:
    data: InitVar[str]
    min: int = field(init=False)
    max: int = field(init=False)

    def __post_init__(self, data: str) -> None:
        left, right = [int(d) for d in data.split("-")]
        self.min = left
        self.max = right

    def fresh(self, id: int) -> bool:
        return id >= self.min and id <= self.max


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
    fresh: int = 0

    for ingredient in ingredients:
        if any([r.fresh(ingredient) for r in ranges]):
            fresh += 1

    print(fresh)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
