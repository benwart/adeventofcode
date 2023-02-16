#!/usr/bin/env python3

import numpy as np

def parse_strs(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


def parse_rows(filepath):
    for line in parse_strs(filepath):
        yield [int(i) for i in line]


def parse_table(filepath):
    t = [r for r in parse_rows(filepath)]
    return np.array(t, dtype=int)


if __name__ == "__main__":
    table = parse_table("./2021/day09/data/example_1")
    print(table)
