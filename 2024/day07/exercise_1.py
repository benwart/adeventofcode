#!/usr/bin/env python

from dataclasses import dataclass
from operator import add, mul
from pathlib import Path
from typing import Callable, Iterable


OPERATORS: dict[str, Callable[[int, int], int]] = {
    "+": add,
    "*": mul,
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


def combinations(sample: str, n: int) -> Iterable[str]:
    m: int = 2**n
    for i in range(m):
        yield "".join(map(lambda c: sample[int(c)], bin(i)[2:].zfill(n)))


def is_calibratable(calibration: Calibration) -> bool:
    length: int = len(calibration.variables) - 1

    # iterate over all combinations of operators - brute force
    for operators in combinations("".join(OPERATORS.keys()), n=length):
        # calculate the result
        result: int = calibration.variables[0]
        for i in range(length):
            op: Callable[[int, int], int] = OPERATORS[operators[i]]
            a: int = result
            b: int = calibration.variables[i + 1]
            result = op(a, b)

        if result == calibration.result:
            return True
        else:
            pass

    return False


def main(filepath: Path):
    total: int = 0
    for calibration in parse_calibrations(filepath):
        if is_calibratable(calibration):
            total += calibration.result

    print(total)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
