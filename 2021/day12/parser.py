#!/usr/bin/env python3

def parse_strs(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


def parse_edges(filepath):
    for line in parse_strs(filepath):
        edges = line.split("-")
        yield edges


if __name__ == "__main__":
    for edges in parse_edges("./2021/day12/data/example_1"):
        e1, e2 = edges
        print(f"{e1}-{e2}")