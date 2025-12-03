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
    output: list[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index: int = -1

    for position in range(0, 11):
        start, stop = index + 1, position - 11
        sub: list[int] = bank[start:stop]
        for i, b in enumerate(sub):
            if b > output[position]:
                output[position] = b
                index = i + start

    for b in bank[index + 1 :]:
        if b > output[11]:
            output[11] = b

    return int("".join([str(o) for o in output]))


def main(filepath: Path):
    total: int = 0
    for line in parse_lines(filepath):
        bank: list[int] = parse_bank(line)
        total += max_jolts_per_bank(bank)

    print(total)


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
