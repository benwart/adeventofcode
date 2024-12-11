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

from pathlib import Path
from typing import Iterable


def digits(stone: int) -> int:
    return len(str(stone))


def parse_lines(filepath: Path) -> Iterable[str]:
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()


def blink(stones: list[int]) -> list[int]:
    new_stones: list[int] = []
    for stone in stones:
        # zero
        if stone == 0:
            new_stones.append(1)
            continue

        # even digits
        stone_str: str = str(stone)
        l: int = len(stone_str)
        if l % 2 == 0:
            split_len: int = l // 2
            new_stones.extend([int(stone_str[:split_len]), int(stone_str[split_len:])])
            continue

        # everything else * 2024
        new_stones.append(stone * 2024)

    return new_stones


def main(filepath: Path):
    stones: list[int] = []
    for line in parse_lines(filepath):
        stones.extend(map(int, line.split(" ")))

    # initial
    print(stones)

    # blink
    for _ in range(25):
        print(".", end="")
        stones = blink(stones)

    print(len(stones))


if __name__ == "__main__":
    main(Path(__file__).parent / "data" / "full")
