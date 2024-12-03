#!/usr/bin/env python

from pathlib import Path
from re import compile, Pattern, Match
from typing import Iterable

mul_func: Pattern = compile(r"(?P<mul>mul)\((?P<a>\d+),(?P<b>\d+)\)|(?P<do>do)\(\)|(?P<dont>don't)\(\)")

def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def main(filepath: Path):
    total: int = 0
    mul_enable: bool = True
    for line in parse_lines(filepath):
        m: Match
        for m in mul_func.finditer(line):
            groups: dict[str, str] = m.groupdict()
            if groups["mul"] and mul_enable:
                total += int(groups["a"]) * int(groups["b"])

            elif groups["do"]:
                mul_enable = True

            elif groups["dont"]:
                mul_enable = False

    print(total)

if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
