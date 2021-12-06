#!/usr/bin/env python3

def parse_strs(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


def parse_fish_ages(filepath):
    full = next(parse_strs(filepath))
    return list(map(int, full.split(",")))


if __name__ == "__main__":
    ages = parse_fish_ages("./2021/day06/data/example_1")
    print(ages)