#!/usr/bin/env python3

from typing import Generator


def parse_lines(filepath: str) -> Generator[str, None, None]:
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


def parse_ints(filepath: str) -> Generator[int, None, None]:
    for line in parse_lines(filepath):
        yield int(line)