#!/usr/bin/env python

from functools import cache
from pathlib import Path
from typing import Iterable


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


@cache
def solve(pattern: str, towels: tuple[str, ...]) -> int:
    if len(pattern) == 0:
        return 1
    else:
        result: int = 0
        for t in towels:
            if pattern.startswith(t):
                result += solve(pattern[len(t) :], towels)

        return result


def main(filepath: Path):
    line_iter: Iterable[str] = parse_lines(filepath)

    towels: set[str] = {t.strip() for t in next(line_iter).strip().split(",")}
    patterns: list[str] = [line.strip() for line in line_iter if len(line) > 0]

    solves: list[int] = [solve(p, tuple(towels)) for p in patterns]
    print(len([s for s in solves if s > 0]))


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
