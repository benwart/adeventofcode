#!/usr/bin/env python

from pathlib import Path
from typing import Iterable


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def parse_data(filepath: Path) -> tuple[dict[int, list[int]], list[list[int]]]:
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

    return rules, manuals


def check_order(rules: dict[int, list[int]], current: int, other: int) -> bool:
    if current in rules and not other in rules[current]:
        return True

    if current not in rules:
        return True

    return False


def fix_order(rules: dict[int, list[int]], manual: list[int]) -> list[int]:
    fixed: list[int] = manual.copy()
    done: bool = False
    while not done:
        for i, page in enumerate(fixed):
            if page in rules:
                before: list[int] = rules[page]
                after: list[int] = fixed[i + 1 :]

                # find the intersection of before values in the after set
                intersection: set[int] = set(before) & set(after)

                # get the last index value of the intersection values
                last: int = -1
                for a in intersection:
                    last = max(after.index(a), last)

                # move the page to be the last index, as the move will shift everything down
                last_index: int = last + i + 1

                if i != last_index:
                    # print(f"{page} -> {last_index}")

                    # move the page to the last index
                    fixed.insert(last_index, fixed.pop(i))
                    break

        if i == len(fixed) - 1:
            done = True

    # print(fixed)
    return fixed


def main(filepath: Path):
    rules: dict[int, list[int]]
    manuals: list[list[int]]

    rules, manuals = parse_data(filepath)

    total: int = 0

    for manual in manuals:
        bad: bool = False
        for i, page in enumerate(manual):
            for j in range(i + 1, len(manual)):
                if not check_order(rules, page, manual[j]):
                    bad = True
                    break

        if bad:
            # fix the order
            fixed: list[int] = fix_order(rules, manual)

            # find the middle number
            middle: int = fixed[len(fixed) // 2]
            total += middle

    print(total)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
