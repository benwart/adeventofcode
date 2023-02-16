#!/usr/bin/env python3

from functools import reduce
from operator import add


def parse_lines(filepath: str):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


def parse_elves(filepath: str):
    elf: list[int] = []
    for line in parse_lines(filepath):

        # all elf values end in empty line
        if not line:
            yield elf
            elf = []
            continue

        # convert to int since input only contains ints
        calories = int(line)
        elf.append(calories)


def main():
    largest = 0
    for elf in parse_elves("2022/day01/data/full"):
        total = reduce(add, elf)
        largest = max(total, largest)

    print(f"largest: {largest}")


if __name__ == "__main__":
    main()
