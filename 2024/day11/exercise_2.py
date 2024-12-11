#!/usr/bin/env python

# As you observe them for a while, you find that the stones have a consistent behavior. Every time
# you blink, the stones each simultaneously change according to the first applicable rule in this list:
#
#  - If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
#  - If the stone is engraved with a number that has an even number of digits, it is replaced by two
#    stones. The left half of the digits are engraved on the new left stone, and the right half of
#    the digits are engraved on the new right stone. (The new numbers don't keep extra leading
#    zeroes: 1000 would become stones 10 and 0.)
#  - If none of the other rules apply, the stone is replaced by a new stone; the old stone's number
#    multiplied by 2024 is engraved on the new stone.

from functools import cache
from math import floor, log10
from pathlib import Path
from typing import Iterable


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


@cache
def blink(x, d=75):
    if d == 0:
        return 1
    if x == 0:
        return blink(1, d - 1)

    l = floor(log10(x)) + 1
    if l % 2 == 0:
        return blink(x // 10 ** (l // 2), d - 1) + blink(x % 10 ** (l // 2), d - 1)

    return blink(x * 2024, d - 1)


def main(filepath: Path):
    input: tuple[int, ...] = ()
    for line in parse_lines(filepath):
        input = map(int, line.split(" "))

    # initial
    print(input)

    # do the solve recursively
    print(sum(map(blink, input)))


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
