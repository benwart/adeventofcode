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
    all = [reduce(add, elf) for elf in parse_elves("2022/day01/data/full")]
    all.sort(reverse=True)
    top_three = all[0:3]

    print(top_three)
    print(reduce(add, top_three))


if __name__ == "__main__":
    main()
