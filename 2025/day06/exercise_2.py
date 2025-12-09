#!/usr/bin/env python

from collections.abc import Callable
from functools import reduce
from operator import mul, add
from pathlib import Path
from typing import Iterable


operation: dict[str, Callable] = {
    "*": mul,
    "+": add,
}


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip("\n")


def vertical(numbers: list[str], i: int) -> str:
    return "".join([n[i] for n in numbers])


def main(filepath: Path):
    inputs: list[str] = [line for line in parse_lines(filepath)]
    numbers: list[str] = inputs[0:-1]
    ops: str = inputs[-1]

    total: int = 0
    vars: list[int] = []
    for i in range(len(ops) - 1, -1, -1):
        v: str = vertical(numbers, i)
        if v.strip():
            vars.append(int(v))

        op: str = ops[i].strip()
        if op:
            answer: int = reduce(operation[op], vars)
            total += answer
            vars = []

    print(total)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
