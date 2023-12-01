#!/usr/bin/env python

from typing import Iterable


def parse_lines(filepath: str) -> Iterable[str]:
    with open(filepath) as f:
        for line in f:
            yield line.strip()


def parse_numbers(filepath: str) -> Iterable[int]:
    for line in parse_lines(filepath):
        numbers = [int(c) for c in line if c.isdigit()]
        yield int(f"{numbers[0]}{numbers[-1]}")


if __name__ == "__main__":
    print(sum(parse_numbers("2023/day01/data/full")))
