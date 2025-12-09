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


def problem(vars: list[list[str]], i: int) -> Iterable[int]:
    for v in range(len(vars)):
        yield int(vars[v][i])


def parse_lines(filepath: Path) -> Iterable[list[str]]:
    with open(filepath, "r") as f:
        for line in f:
            yield [c for c in line.strip().split() if c]


def main(filepath: Path):
    inputs: list[list[str]] = [line for line in parse_lines(filepath)]
    variables: list[list[str]] = inputs[0:-1]
    operations: list[str] = inputs[-1]

    length: int = len(variables[0])
    total: int = 0
    for i in range(length):
        total += reduce(operation[operations[i]], problem(variables, i))

    print(total)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
