#!/usr/bin/env python3

from collections import namedtuple

Point = namedtuple("Point", "y x")
Fold = namedtuple("Fold", "axis value")


def parse_strs(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


def parse_page(filepath):
    dots = list()
    folds = list()

    strs = parse_strs(filepath)
    
    # parse dots
    for line in strs:
        if len(line) == 0:
            break
        x,y = line.split(",")
        dots.append(Point(int(y), int(x)))
    
    # parse folds
    for line in strs:
        if len(line) == 0:
            break
        axis, value = line.split(" ")[2].split("=")
        folds.append(Fold(axis, int(value)))

    return dots, folds


if __name__ == "__main__":
    dots, folds = parse_page("./2021/day13/data/example_1")
    print(dots, folds)