#!/usr/bin/env python3


def parse_lines(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


def parse_ints(filepath):
    for line in parse_lines(filepath):
        yield int(line)