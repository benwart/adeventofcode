#!/usr/bin/env python

from pathlib import Path
from typing import Iterable

"""
- The levels are either all increasing or all decreasing.
- Any two adjacent levels differ by at least one and at most three.
"""


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()

def parse_reports(filepath: Path) -> Iterable[list[int]]:
    for line in parse_lines(filepath):
        yield [int(value) for value in line.split(" ")]


def check_report(report: list[int]) -> bool:
    if len(report) < 2:
        print("Report too short")

    combined = zip(report[0:-2], report[1:-1])

    deltas: list[int] = []
    for left, right in zip(report[0:-1], report[1:]):
        deltas.append(left - right)

    increasing: bool = all(3 >= d >= 1 for d in deltas)
    decreasing: bool = all(-3 <= d <= -1 for d in deltas)

    safe: bool = increasing or decreasing
    return safe


def main(filepath: Path):
    count: int = 0
    for report in parse_reports(filepath):
        safe: bool = check_report(report)
        if safe:
            count += 1

    print(count)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
