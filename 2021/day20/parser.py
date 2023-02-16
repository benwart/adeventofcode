#!/usr/bin/env python3

def parse_strs(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


lookup = {
    ".": 0,
    "#": 1,
}

def parse_data(filename):
    strs = parse_strs(filename)
    algo = [ lookup[s] for s in next(strs) ]

    image = []
    for line in strs:
        if len(line):
            image.append([ lookup[s] for s in line])
    
    return algo, image


if __name__ == "__main__":
    a, i = parse_data("./2021/day20/data/example_1")
    print(a)
    print(i)