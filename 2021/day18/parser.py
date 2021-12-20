#!/usr/bin/env python3

import json

from typing import Union

Number = list[Union[str, int]]


def parse_strs(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


def parse_json(filepath):
    for line in parse_strs(filepath):
        yield json.loads(line)


class Pair(object):
    def __init__(self, j):
        l, r = j
        self.l = l if isinstance(l, int) else Pair(l)
        self.r = r if isinstance(r, int) else Pair(r)

    def dump(self) -> Number:
        output = ["["]
        output += [self.l] if isinstance(self.l, int) else self.l.dump()
        output += [self.r] if isinstance(self.r, int) else self.r.dump()  
        output += ["]"]
        
        return output

    def __str__(self) -> str:
        return "".join([
            "[",
            str(self.l),
            ",",
            str(self.r),
            "]",
        ])


def parse_number(filepath) -> Number:
    for j in parse_json(filepath):
        p = Pair(j)
        # print(p)
        yield p.dump()


if __name__ == "__main__":
    for n in parse_number("./2021/day18/data/example_1"):
        print(n)