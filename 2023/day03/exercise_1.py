#!/usr/bin/env python

from pathlib import Path
from re import finditer
from typing import Iterable


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def check(data: str) -> bool:
    filtered = [c for c in data if c != "." and not c.isdigit()]
    return len(filtered) > 0


def main(filepath: Path):
    input = list(parse_lines(filepath))

    # pad the input
    length = len(input[0]) + 2
    input = [
        "." * length,
        *[f".{i}." for i in input],
        "." * length,
    ]

    total = 0
    for index, line in enumerate(input):
        print(line)
        for match in finditer(r"(\d+)", line):
            print(match.group(1))
            first, last = match.regs[0]
            checks = [
                check(input[index - 1][first - 1 : last + 1]),  # above
                check(input[index][first - 1 : first]),  # left
                check(input[index][last : last + 1]),  # right
                check(input[index + 1][first - 1 : last + 1]),  # below
            ]

            if any(checks):
                total += int(match.group(1))

    print(total)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
