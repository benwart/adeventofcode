#!/usr/bin/env python

from collections import deque
from copy import copy
from dataclasses import dataclass, field
from itertools import product
from pathlib import Path
from typing import Deque, Iterable


def validate_groups(springs: list[str], check: list[str]) -> bool:
    """Return a list of groups of disabled springs."""
    groups = []
    group = 0

    for spring in springs:
        # short circuit if the group are already wrong
        if len(groups) > 0 and groups != check[: len(groups)]:
            break

        if spring == "#":
            group += 1

        else:
            if group > 0:
                groups.append(group)
                group = 0

    # make sure to grab any open groups
    if group > 0:
        groups.append(group)

    return groups == check


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

    def replace(self, replacement: Deque[str]) -> list[str]:
        """Replace the unknowns with the replacement."""
        replaced = copy(self.springs)

        for i in self.unknowns:
            replaced[i] = replacement.popleft()

        return replaced


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def parse_report(filepath: Path) -> Iterable[ConditionReport]:
    for line in parse_lines(filepath):
        springs, groups = line.split(" ")
        yield ConditionReport(
            [s for s in springs],
            [int(group) for group in groups.split(",")],
        )


def check_all_permutations(report: ConditionReport) -> int:
    """Check all permutations of the springs."""
    permutations = product(["#", "."], repeat=len(report.unknowns))
    valid = 0

    for p in permutations:
        match = sum([1 for c in p if c == "#"])

        # short circuit if the group are already wrong
        if match != report.must_match:
            continue

        replaced = report.replace(deque(p))
        if validate_groups(replaced, report.groups):
            valid += 1

    return valid


def main(filepath: Path):
    total = 0
    for report in parse_report(filepath):
        print(report)
        possible = check_all_permutations(report)
        print(f"Possible: {possible} for {report}")
        total += possible

    print(f"Total: {total}")


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
