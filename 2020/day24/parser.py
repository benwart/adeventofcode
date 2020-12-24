#!/usr/bin/env python3

import re

from collections import namedtuple


def parse_lines(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


DIR_REGEX = re.compile(f"se|sw|nw|ne|e|w")

DIR_TRANSFORM = {
    "e": (1, -1, 0),
    "ne": (1, 0, -1),
    "nw": (0, 1, -1),
    "w": (-1, 1, 0),
    "sw": (-1, 0, 1),
    "se": (0, -1, 1),
}

Dir = namedtuple("Dir", ("raw", "transform"))


def parse_direction(line):
    miter = DIR_REGEX.finditer(line)
    return [Dir(m.group(0), DIR_TRANSFORM[m.group(0)]) for m in miter]


def parse_input(filepath):
    for line in parse_lines(filepath):
        yield parse_direction(line)


if __name__ == "__main__":
    print([dir for dir in parse_input("./data/example1")])