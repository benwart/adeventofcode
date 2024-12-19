#!/usr/bin/env python

from collections import deque
from itertools import product
from pathlib import Path
from typing import Iterable


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def towels_per_stripe(pattern: str, i: int, towels: list[str]) -> list[str]:
    return [towel for towel in towels if towel == pattern[i : i + len(towel)]]


def solve(pattern: str, towels: list[str]) -> bool:
    possible: list[list[str]] = []
    for i, _ in enumerate(pattern):
        matches: list[str] = towels_per_stripe(pattern, i, towels)

        # if the first stripe doesn't have any matches then it's not possible
        if i == 0 and len(matches) == 0:
            # print(f"F: {pattern}")
            return False

        # make sure each stripe has at least one match (even if it's an empty string)
        possible.append(matches if len(matches) else [" "])

    for option in product(*possible):
        output: deque = deque()
        o: int = 0
        while o < len(option):
            opt: str = option[o]
            if opt == " ":
                break
            output.append(opt)
            o += len(opt)

        combined: str = "".join(output)
        if combined == pattern:
            # print(f"T: {pattern} == {combined}")
            return True

    # print(f"F: {pattern} {possible}")
    return False


def main(filepath: Path):
    line_iter: Iterable[str] = parse_lines(filepath)

    towels: list[str] = [t.strip() for t in next(line_iter).strip().split(",")]
    patterns: list[str] = [line.strip() for line in line_iter if len(line) > 0]

    count: int = 0
    for pattern in patterns:
        result: bool = solve(pattern, towels)
        print("+" if result else ".", end="")
        if result:
            count += 1

    print(count)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
