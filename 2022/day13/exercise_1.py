#!/usr/bin/env python3

from typing import Iterable
from json import loads


def parse_lines(filepath: str) -> Iterable[str]:
    with open(filepath) as f:
        for line in f:
            yield line.strip()


def parse_pairs(filepath: str):
    lines = []
    for line in parse_lines(filepath):
        if not line:
            yield lines
            lines = []
        else:
            lines.append(loads(line))

    if lines:
        yield lines[0], lines[1]


def main():
    for left, right in parse_pairs("data/example_1"):
        print(left)
        print(right)
        print()


if __name__ == "__main__":
    main()
