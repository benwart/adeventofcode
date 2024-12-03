#!/usr/bin/env python

from pathlib import Path
from re import compile, Pattern, Match
from typing import Iterable

mul_func: Pattern = compile(r"mul\((?P<a>\d+),(?P<b>\d+)\)")

def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def main(filepath: Path):
    total: int = 0
    for line in parse_lines(filepath):
        funcs: list[Match] = mul_func.findall(line)
        total += sum([int(a) * int(b) for a,b in funcs])

    print(total)

if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
