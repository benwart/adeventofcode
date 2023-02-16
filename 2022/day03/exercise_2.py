#!/usr/bin/env python3

from functools import reduce
from operator import add


def parse_lines(filepath: str):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


def parse_rucksacks(filepath: str):
    for line in parse_lines(filepath):
        yield set(line)


def parse_groups(filepath: str):
    group = []
    for rucksack in parse_rucksacks(filepath):
        if len(group) == 3:
            yield set.intersection(*group)
            group = []

        group.append(rucksack)

    # return the last group
    yield set.intersection(*group)


lower_offset = 0 - 96
upper_offset = (0 - 64) + 26


def compute_priority(letter: str) -> int:
    index = ord(letter)
    return index + upper_offset if letter.isupper() else index + lower_offset


def main():
    prioties = [
        compute_priority(letter.pop())
        for letter in parse_groups("2022/day03/data/full")
    ]
    total = reduce(add, prioties)
    print(total)


if __name__ == "__main__":
    main()
