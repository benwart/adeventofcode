#!/usr/bin/env python

from pathlib import Path
from typing import Iterable


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def parse_bank(line: str) -> list[int]:
    return [int(b) for b in line]


def max_jolts_per_bank(bank: list[int]) -> int:
    output: list[int] = [0, 0]
    index: int = 0
    for i, b in enumerate(bank[:-1]):
        if b > output[0]:
            output[0] = b
            index = i

    for b in bank[index + 1 :]:
        if b > output[1]:
            output[1] = b

    return int("".join([str(o) for o in output]))


def main(filepath: Path):
    total: int = 0
    for line in parse_lines(filepath):
        bank: list[int] = parse_bank(line)
        total += max_jolts_per_bank(bank)

    print(total)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
