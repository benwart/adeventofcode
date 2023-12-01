#!/usr/bin/env python

from re import compile
from typing import Iterable


def parse_lines(filepath: str) -> Iterable[str]:
    with open(filepath) as f:
        for line in f:
            yield line.strip()


spelled_numbers = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

SPELLED_PATTERN = "|".join(spelled_numbers.keys())
F_NUMBER_REGEX = compile(f"(?P<number>[1-9]|{SPELLED_PATTERN}).*")
L_NUMBER_REGEX = compile(f".*(?P<number>[1-9]|{SPELLED_PATTERN})")


def find_first_and_last(line: str) -> int:
    first = F_NUMBER_REGEX.search(line).groupdict()["number"]
    last = L_NUMBER_REGEX.search(line).groupdict()["number"]
    return int(f"{spelled_numbers.get(first, first)}{spelled_numbers.get(last, last)}")


def parse_numbers(filepath: str) -> Iterable[int]:
    for line in parse_lines(filepath):
        yield find_first_and_last(line)


if __name__ == "__main__":
    print(sum(parse_numbers("2023/day01/data/full")))
