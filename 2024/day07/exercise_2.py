#!/usr/bin/env python

from dataclasses import dataclass
from operator import add, mul
from pathlib import Path
from typing import Callable, Iterable


OPERATORS: dict[str, Callable[[int, int], int]] = {
    "+": add,
    "*": mul,
    "|": lambda a, b: int(f"{a}{b}"),
}


@dataclass
class Calibration:
    result: int
    variables: list[int]


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def parse_calibrations(filepath: Path) -> Iterable[Calibration]:
    for line in parse_lines(filepath):
        result: str
        variables: str
        [result, variables] = line.split(":")
        calibration: Calibration = Calibration(int(result), list(map(int, variables.strip().split(" "))))
        yield calibration


def ternary(n):
    if n == 0:
        return "0"
    nums = []
    while n:
        n, r = divmod(n, 3)
        nums.append(str(r))
    return "".join(reversed(nums))


def combinations(sample: str, n: int) -> Iterable[str]:
    m: int = 3**n
    for i in range(m):
        output: str = "".join(map(lambda c: sample[int(c)], ternary(i).zfill(n)))
        yield output


def is_calibratable(calibration: Calibration) -> bool:
    length: int = len(calibration.variables) - 1
    sample: str = "".join(OPERATORS.keys())

    # iterate over all combinations of operators - brute force
    for operators in combinations(sample, n=length):
        # calculate the result
        result: int = calibration.variables[0]
        for i in range(length):
            op: Callable[[int, int], int] = OPERATORS[operators[i]]
            a: int = result
            b: int = calibration.variables[i + 1]
            result = op(a, b)

        if result == calibration.result:
            return True

    return False


def main(filepath: Path):
    total: int = 0
    for calibration in parse_calibrations(filepath):
        found: bool = is_calibratable(calibration)
        if found:
            total += calibration.result

    print(total)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
