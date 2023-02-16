#!/usr/bin/env python3

from collections import defaultdict
from parser import parse_data

original = {
    0: "abcefg",
    1: "cf",
    2: "acdeg",
    3: "acdfg",
    4: "bcdf",
    5: "abdfg",
    6: "abdefg",
    7: "acf",
    8: "abcdefg",
    9: "abcdfg",
}

def group_by_len(input):
    grouped = defaultdict(list)
    for i in input:
        grouped[len(i)].append(set(i))
    return grouped


def solve_a(lens):

    # find 7 and 1 by len
    n1 = lens[2][0]
    n7 = lens[3][0]

    # find set of letters from 7 not in 1
    a = n7 - n1
    return a.pop()


def solve_bd(lens):
    # get 4 and 1 by len
    n1 = lens[2][0]
    n4 = lens[4][0]

    bd = n4 - n1

    for s in lens[6]:
        if not bd <= s:
            # found 0
            n0 = s
            break

    d = bd - n0
    b = bd - d

    return b.pop(), d.pop()


def solve_cfg(lens, m):
    # get 4 and 1 by len
    n1 = lens[2][0]
    n4 = lens[4][0]
    bd = n4 - n1

    for s in lens[5]:
        if bd <= s:
            # found 5
            n5 = s
            break

    a = set(m["a"])
    b = set(m["b"])
    d = set(m["d"])

    g = (n5 - n4) - set(m["a"])
    f = n5 - a - b - d - g
    c = n1 - f

    return c.pop(), f.pop(), g.pop()
    

def solve_e(lens, m):
    n8 = lens[7][0]
    s = n8
    for v in m.values():
        s -= set(v)

    e = s
    return e.pop()


def number_sets(o, m):
    output = {}
    for n, segs in o.items():
        k = frozenset([m[l] for l in segs])
        output[k] = str(n)
    return output


outputs = []
for input, output in parse_data("./2021/day08/data/full"):

    m = {}

    # figure out the segment mapping
    lens = group_by_len(input)
    m["a"] = solve_a(lens)
    m["b"], m["d"] = solve_bd(lens)
    m["c"], m["f"], m["g"] = solve_cfg(lens, m)
    m["e"] = solve_e(lens, m)

    # generate numbers from mapping
    numbers = number_sets(original, m)

    # lookup numbers from ouput 
    o = int(''.join(map(lambda o: numbers[frozenset(o)], output)))
    outputs.append(o)

print(sum(outputs))
