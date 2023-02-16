#!/usr/bin/env python3

from dataclasses import dataclass, field, InitVar


@dataclass
class Section:
    start: int = field(init=False)
    finish: int = field(init=False)
    start_str: InitVar[str]
    finish_str: InitVar[str]

    def __post_init__(self, start_str: str, finish_str: str):
        self.start = int(start_str)
        self.finish = int(finish_str)


def parse_lines(filepath: str):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


def parse_pairs(filepath: str):
    for line in parse_lines(filepath):
        first, second = line.split(",")
        yield Section(*first.split("-")), Section(*second.split("-"))


def overlapping_sections(first, second) -> bool:
    a = first.start >= second.start
    b = first.finish <= second.finish

    # print(f"{a} and {b} == {a and b}")

    return first.start >= second.start and first.finish <= second.finish


def main():
    count = 0
    for first, second in parse_pairs("2022/day04/data/full"):
        if overlapping_sections(first, second) or overlapping_sections(second, first):
            count += 1

    print(count)


if __name__ == "__main__":
    main()
