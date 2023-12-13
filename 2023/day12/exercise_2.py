#!/usr/bin/env python

from dataclasses import dataclass, field
from functools import cache
from pathlib import Path
from typing import Iterable


@cache
def find_solutions(springs, sizes, group_size=0):
    # Dynamic programming solution using the cache to significantly speed up the processing
    # Run through each item in the string, if it's a question mark, try all options replacing each with either . or #
    # If the replacement results in a successful line, return one and continue
    if (
        not springs
    ):  # Return 1 if there are no more group sizes and there is no current group
        return not sizes and not group_size
    num_solutions = 0
    symbol = [".", "#"] if springs[0] == "?" else springs[0]
    for sym in symbol:
        if sym == "#":  # If it's # expand the group
            num_solutions += find_solutions(springs[1:], sizes, group_size + 1)
        else:
            if (
                group_size
            ):  # If the . is at the end of a group and it matches the first size, continue
                if sizes and sizes[0] == group_size:
                    num_solutions += find_solutions(springs[1:], sizes[1:])
            else:  # If the . is at the end of a group and it doesn't match the first size, continue without removing a group
                num_solutions += find_solutions(springs[1:], sizes)
    return num_solutions


@dataclass
class ConditionReport:
    springs: list[str]
    groups: list[int]
    unknowns: list[int] = field(init=False)
    must_match: int = field(init=False)

    def __post_init__(self):
        self.must_match = sum(self.groups) - len([s for s in self.springs if s == "#"])
        self.unknowns = [i for i, s in enumerate(self.springs) if s == "?"]

    def __str__(self):
        return f"{''.join(self.springs)} {self.groups}"


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def parse_report(filepath: Path) -> Iterable[ConditionReport]:
    for line in parse_lines(filepath):
        springs, groups = line.split(" ")

        springs = "?".join([springs for _ in range(5)])
        groups = ",".join([groups for _ in range(5)])

        yield ConditionReport(
            [s for s in springs],
            [int(group) for group in groups.split(",")],
        )


def main(filepath: Path):
    total = 0
    for report in parse_report(filepath):
        print(report)
        possible = find_solutions(
            str("".join(report.springs + ["."])), tuple(report.groups)
        )
        print(f"Possible: {possible} for {report}")
        total += possible

    print(f"Total: {total}")


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
