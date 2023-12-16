#!/usr/bin/env python

from pathlib import Path
from typing import Iterable


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def hash_string(string: str) -> int:
    acc = 0
    for c in string:
        acc += ord(c)
        acc *= 17
        acc = acc % 256

    return acc


def parse_init_sequence(filepath: Path) -> list[str]:
    line = next(parse_lines(filepath))
    values = line.split(",")
    sequence = [hash_string(v) for v in values if v]

    return sequence


def main(filepath: Path):
    sequeence = parse_init_sequence(filepath)
    total = sum(sequeence)
    print(f"Total: {total}")


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
