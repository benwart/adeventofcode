#!/usr/bin/env python3


import numpy as np

from typing import Iterable
from parser import parse_page, Point, Fold

def print_array(arr):
    print_mapping = {0: ".", 1: "#"}
    print_keys = {"int": lambda n: print_mapping[n]}
    np.set_printoptions(formatter=print_keys)
    print(arr, end="\n\n")
    np.set_printoptions(formatter=None)


def max_xy(values:Point):
    max_x = max(values, key=lambda p: p.x).x + 1
    max_y = max(values, key=lambda p: p.y).y + 1

    return max_y, max_x


def get_page_with_dots(dots:Iterable[Point]):
    page = np.zeros(max_xy(dots), dtype=int)

    for d in dots:
        page[d.y, d.x] = 1

    return page


def fold_page_up(page, value):
    t = page[0:value,:]
    b = page[value+1:,:]
    b = np.flipud(b)

    # create proper sized array for large section

    # copy the smaller section to proper location
    np.copyto(t, b, where=b == 1)

    # return copy of folded output

    return page

def fold_page_left(page, value):
    l = page[:,0:value]
    r = page[:,value+1:]
    r = np.fliplr(r)

    return page

if __name__ == "__main__":
    dots, folds = parse_page("./2021/day13/data/example_1")

    # load data into np array
    page = get_page_with_dots(dots)

    # show start
    print_array(page)
    
    # only perform first fold
    fold = folds[0]
    if fold.axis == "y":
        page = fold_page_up(page, fold.value)
    elif fold.axis == "x":
        page = fold_page_left(page, fold.value)

    print(page)