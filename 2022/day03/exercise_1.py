#!/usr/bin/env python3

from functools import reduce
from operator import add


def parse_lines(filepath: str):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


def parse_rucksacks(filepath: str):
    for line in parse_lines(filepath):
        both = len(line)
        compartment_size = int(both / 2)

        first = set(line[0:compartment_size])
        second = set(line[compartment_size:])

        yield first.intersection(second)


lower_offset = 0 - 96
upper_offset = (0 - 64) + 26


def compute_priority(letter: str) -> int:
    index = ord(letter)
    return index + upper_offset if letter.isupper() else index + lower_offset


def main():
    prioties = [
        compute_priority(letter.pop())
        for letter in parse_rucksacks("2022/day03/data/full")
    ]
    total = reduce(add, prioties)
    print(total)


if __name__ == "__main__":
    main()
