#!/usr/bin/env python

from pathlib import Path
from typing import Iterable


def parse_lines(filepath: Path) -> Iterable[list[str]]:
    with open(filepath, "r") as f:
        for line in f:
            yield [c for c in line.strip()]


def beams(line: list[str]) -> Iterable[int]:
    for i, c in enumerate(line):
        if c == "|":
            yield i


def main(filepath: Path):
    lines: list[list[str]] = [line for line in parse_lines(filepath)]

    splits: int = 0
    for r in range(0, len(lines) - 1):
        line: list[str] = lines[r]
        below: list[str] = lines[r + 1]

        if "S" in line:
            below[line.index("S")] = "|"

        for i in beams(line):
            if below[i] == ".":
                below[i] = "|"

            elif below[i] == "^":
                splits += 1
                below[i - 1] = "|"
                below[i + 1] = "|"

        print("".join(lines[r]))

    print(splits)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "example_1")
