#!/usr/bin/env python3

import numpy as np
from numpy.lib.stride_tricks import as_strided
from parser import parse_initial

dtype = np.uint8


def print_array(arr):
    print_mapping = {0: ".", 1: "#"}
    print_keys = {"int": lambda n: print_mapping[n]}
    np.set_printoptions(formatter=print_keys)
    print(arr, end="\n\n")
    np.set_printoptions(formatter=None)


def expand_array(arr):
    exp_size = tuple(i + 2 for i in arr.shape)
    exp = np.zeros(exp_size, dtype=np.uint8)
    nd_slice = (slice(1, -1),) * len(arr.shape)
    exp[nd_slice] = arr
    return exp


def neighborhood_strides(arr):
    assert all(len > 2 for len in arr.shape)

    ndims = len(arr.shape)
    new_shape = [len - 2 for len in arr.shape]
    new_shape.extend([3] * ndims)

    strides = arr.strides + arr.strides
    return as_strided(arr, shape=new_shape, strides=strides)


def init_iteration(state):
    # setup initial simulation state
    full = expand_array(state)
    nd_slice = (slice(1, -1),) * len(state.shape)
    board = full[nd_slice]
    ndims = len(board.shape)
    return full, board, ndims


# index is number of neighbors alive
rules = {
    "alive": np.zeros(80 + 1, np.uint8),
    "dead": np.zeros(80 + 1, np.uint8),
}
rules["alive"][[2, 3]] = 1
rules["dead"][3] = 1

# fetch initial state from file
initial = parse_initial("./data/full")
iterations = 6

# set size to make the iteratiosn easier
state = np.zeros([initial.shape[0]] * 4, dtype=dtype)
state[1, 1] = initial
state = expand_array(state)

for i in range(1, iterations + 1):
    print(f"Cycle: {i-1} (Active: {state.sum()})")
    full, board, ndims = init_iteration(state)

    neighborhoods = neighborhood_strides(full)
    sum_over = tuple(-(i + 1) for i in range(ndims))
    neighbor_count = np.sum(neighborhoods, sum_over) - board

    board[:] = np.where(
        board, rules["alive"][neighbor_count], rules["dead"][neighbor_count]
    )
    state = full

print(f"Cycle: {iterations} (Active: {state.sum()})")