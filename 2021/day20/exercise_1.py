#!/usr/bin/env python3

import numpy as np

from collections import namedtuple
from parser import parse_data

Coord = namedtuple("Coord", "y x")

def print_array(arr):
    print_mapping = {0: ".", 1: "#"}
    print_keys = {"int": lambda n: print_mapping[n]}
    np.set_printoptions(formatter=print_keys)
    print(arr, end="\n\n")
    np.set_printoptions(formatter=None)


def create_np_image(input: list[list[int]]) -> np.array:
    arr = np.array(input, dtype=int)
    arr = np.pad(arr, 2, mode='constant', constant_values=0)
    return arr


def calc_pixel_kernel(a: np.array, c: Coord):
    k = [
        a[c.y-1, c.x-1], a[c.y-1, c.x], a[c.y-1, c.x+1],
        a[c.y, c.x-1],   a[c.y, c.x],   a[c.y, c.x+1],
        a[c.y+1, c.x-1], a[c.y+1, c.x], a[c.y+1, c.x+1],
    ]

    lookup = int("".join(map(lambda i: str(i), k)), base=2)

    return lookup


if __name__ == "__main__":
    algo, input = parse_data("./2021/day20/data/example_1")

    image = create_np_image(input)

    for _ in range(0, 2):
        output = np.zeros(image.shape, dtype=int)

        # since the image is already larger than input
        # only compute data 1 row/col in from edges
        for y in range(1, image.shape[0]-1):
            for x in range(1, image.shape[1]-1):
                c = Coord(y, x)
                l = calc_pixel_kernel(image, c)
                a = algo[l]
                output[y, x] = a

        # use output as input for next iteration
        image = np.pad(output, 2, mode='constant', constant_values=0)

    print_array(output)
    print(np.sum(output))
    