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

    deltas: list[int] = []
    for left, right in zip(report[0:-1], report[1:]):
        deltas.append(left - right)

    increasing: bool = all(3 >= d >= 1 for d in deltas)
    decreasing: bool = all(-3 <= d <= -1 for d in deltas)

    safe: bool = increasing or decreasing
    return safe


def check_variations(report: list[int]) -> bool:
    for skip in range(len(report)):
        if check_report([l for i, l in enumerate(report) if i != skip]):
            return True
    
    return False

def main(filepath: Path):
    """
    Reads a file of reports, counts the number of safe reports, and prints it.

    A report is safe if it is either all increasing or all decreasing, and any two
    adjacent levels differ by at least one and at most three.

    If a report is not safe, it checks all variations of the report which are
    the same but for one level removed. If any variation is safe, then the
    original report is considered safe.

    :param filepath: The file to read.
    :type filepath: Path
    """
    count: int = 0
    for report in parse_reports(filepath):
        safe: bool = check_report(report)
        if safe:
            count += 1
        else:
            safe = check_variations(report)
            if safe:
                count += 1

    print(count)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
