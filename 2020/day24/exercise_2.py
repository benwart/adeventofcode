#!/usr/bin/env python3

import numpy as np

from exercise_1 import exercise_1
from scipy import ndimage


def calculate_shape(c1, c2):
    s = [0 for _ in range(len(c1))]
    for i in range(len(c1)):
        s[i] = abs(c1[i] - c2[i]) + 1
    return tuple(s)


def calculate_offset(min_coords):
    return tuple([abs(i) for i in min_coords])


def apply_offset(offset, coord):
    return tuple(sum(i) for i in zip(*[t for t in [coord, offset]]))


def initialize_board(seed):
    # find the bounds of the seed
    min_coords = tuple(min(i) for i in zip(*[t for t in seed]))
    max_coords = tuple(max(i) for i in zip(*[t for t in seed]))

    # offset and split seed to fit in board
    offset = calculate_offset(min_coords)
    seed_offset = list(map(lambda s: apply_offset(offset, s), seed))
    seed_q, seed_r = zip(*seed_offset)

    # setup board
    shape = calculate_shape(min_coords, max_coords)
    board = np.zeros(shape, dtype=dtype)

    # initialize seed values
    board[seed_q, seed_r] = 1

    return board


def initialize_iteration(last):
    # copy and expand last to make sure there is enough
    # room on the board...going to get slower each iteration
    shape = tuple(i + 2 for i in last.shape)
    board = np.zeros(shape, dtype=dtype)

    # [1:-1,1:-1,...]
    nd_slice = (slice(1, -1),) * len(last.shape)

    # update new board with previous values centered on board
    board[nd_slice] = last
    return board


# rules

BLACK_TILE_RULE = [0, 0, 0, 0, 0, 0, 0, 1, 1]
WHITE_TILE_RULE = [0, 0, 1, 0, 0, 0, 0, 0, 0]

# setup
dtype = np.uint8
seed = list(
    map(
        lambda t: (t[0], t[2]),
        exercise_1("./data/full"),
    )
)

# play game of life

last = initialize_board(seed)

# 100 iterations
iterations = 100

# convolution kernel
k = np.array(
    [
        [0, 1, 1],
        [1, 0, 1],
        [1, 1, 0],
    ]
)

for i in range(1, iterations + 1):
    print(f"Cycle: {i-1} (Active: {last.sum()})")
    board = initialize_iteration(last)
    neighbors = ndimage.convolve(board, k, mode="constant", cval=0)

    # print(neighbors, "\n")
    # print(board, "\n")

    last = (
        ((board == 1) & (neighbors >= 1) & (neighbors <= 2))
        | ((board == 0) & (neighbors == 2))
    ).astype(dtype)

print(f"Cycle: {iterations} (Active: {last.sum()})")