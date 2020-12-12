from enum import Enum


def parse_str(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


class Location(Enum):
    SEAT = 1
    FLOOR = 2


mapping = {
    "L": Location.SEAT,
    ".": Location.FLOOR,
}


def parse_locations(filepath):
    for line in parse_str(filepath):
        yield [d for d in map(lambda x: mapping[x], line)]
