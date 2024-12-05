#!/usr/bin/env python

from pathlib import Path
from typing import Iterable


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def check_order(rules: dict[int, list[int]], current: int, other: int) -> bool:
    if current in rules and not other in rules[current]:
        return True

    if current not in rules:
        return True

    return False


def main(filepath: Path):
    rules: dict[int, list[int]] = {}
    manuals: list[list[int]] = []

    for line in parse_lines(filepath):
        if "|" in line:
            [b, a] = line.split("|")

            before = int(b)
            after = int(a)

            if after not in rules:
                rules[after] = [before]
            else:
                rules[after].append(before)

        if "," in line:
            manuals.append([int(i) for i in line.split(",")])

    total: int = 0

    for manual in manuals:
        good: bool = True
        for i, page in enumerate(manual):
            for j in range(i + 1, len(manual)):
                if not check_order(rules, page, manual[j]):
                    good = False
                    break

        if good:
            # find the middle number
            middle: int = manual[len(manual) // 2]
            total += middle

    print(total)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
