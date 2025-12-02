#!/usr/bin/env python

from pathlib import Path
from typing import Iterable


def parse_lines(filepath: Path) -> Iterable[tuple[str, int]]:
    with open(filepath, "r") as f:
        for line in f:
            clean: str = line.strip()
            yield clean[0], int(clean[1:])


def main(filepath: Path):
    output: int = 0
    value: int = 50
    for direction, steps in parse_lines(filepath):
        value = (value + steps if direction == "R" else value - steps) % 100
        if value == 0:
            output += 1

    print(output)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "example_1")
