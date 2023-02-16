#!/usr/bin/env python3

def parse_strs(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


if __name__ == "__main__":
    for line in parse_strs("./2021/day10/data/example_1"):
        print(line)
