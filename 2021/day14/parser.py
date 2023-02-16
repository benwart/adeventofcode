#!/usr/bin/env python3


def parse_strs(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


def parse_data(filepath):

    strs = parse_strs(filepath)
    template = next(strs)

    insertions = dict()
    for line in strs:
        if len(line) == 0:
            continue

        search, insert = line.split(" -> ")
        insertions[search] = insert
    
    return template, insertions


if __name__ == "__main__":
    template, insertions = parse_data("./2021/day14/data/example_1")
    print(template)
    print(insertions)
