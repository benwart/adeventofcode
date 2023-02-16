import numpy as np


def parse_lines(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


mapping = {
    ".": 0,
    "#": 1,
}


def parse_initial(filepath):
    initial = []
    for line in parse_lines(filepath):
        initial.append([mapping[c] for c in line])

    return np.array(initial, dtype=np.int8)
