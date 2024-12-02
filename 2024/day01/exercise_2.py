#!/usr/bin/env python

from itertools import groupby
from pathlib import Path
from re import compile, Pattern, Match
from typing import Iterable


columns_regex: Pattern = compile(r"(?P<left>\d+)\s+(?P<right>\d+)")

def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()

def main(filepath: Path):
    left: list[int] = []
    right: list[int] = []

    for line in parse_lines(filepath):
        m: Match | None = columns_regex.match(line)
        if m:
            groups: dict[str, str] = m.groupdict()
            left.append(int(groups["left"]))
            right.append(int(groups["right"]))
        else:
            print(f"Unknown line: {line}")
            continue

    right = sorted(right)
    counts: dict[int, int] = {}
    for k, g in groupby(right):
        counts[k] = len(list(g))

    sum: int = 0
    for l in left:
        if l in counts: 
            sum += l* counts[l]

    print(sum)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
