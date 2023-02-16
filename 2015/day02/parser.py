#!/usr/bin/env python3

import re

dim_regex = re.compile(r"(?P<l>\d+)x(?P<w>\d+)x(?P<h>\d+)")


def parse_sides(line):
    return {k: int(v) for k, v in dim_regex.match(line).groupdict().items()}


def parse(filepath):
    with open("./data/full") as f:
        for line in f:
            yield parse_sides(line)
