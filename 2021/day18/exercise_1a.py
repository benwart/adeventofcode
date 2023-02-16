#!/usr/bin/env python3

from parser import parse_json
from typing import Union


class Literal(object):
    def __init__(self, value: int):
        self.value = value

    def __eq__(self, other: "Literal") -> bool:
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)

    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return str(self)


class Pair(object):
    def __init__(self, input: Union[int, list], depth: int = 0, parent: "Pair"=None):
        l, r = input
        self.left = Literal(l) if isinstance(l, int) else Pair(l, depth+1, self)
        self.right = Literal(r) if isinstance(r, int) else Pair(r, depth+1, self)
        self.parent = parent

    def to_list(self) -> list[Union["Pair", Literal]]:
        return [self.left, self.right]

    def zero_pair(self, p: "Pair"):
        zero = Literal(0)

        if self.left is p:
            self.left = zero
        elif self.right is p:
            self.right = zero
        else:
            # didn't find pair so do nothing
            pass

    def __str__(self):
        return str(f"[{self.left},{self.right}]")

    def __repr__(self):
        return f"Pair({str(self)})"


isliteral = lambda o: isinstance(o, Literal)
ispair = lambda o: isinstance(o, Pair)


def add_left_first_literal(p: Pair, l: Literal=None):
    if l is None:
        add_left_first_literal(p.parent, p.left)
        return

    if isliteral(p.right):
        p.right += l.value
        return

    if isliteral(p.left):
        p.left += l.value
        return

    if p.parent is None:
        return

def add_right_first_literal(p: Pair):
    pass


def explode(p: Pair, depth: int=0) -> bool:
    """
    If possible explode a pair.
    
    Rules for Exploding a Pair:
    1. left value is added to the first Literal on the left (if any)
    2. right value is added to the first Literal on the right (if any)
    3. replace the pair with Literal(0)
    """

    curr: Pair = p
    boom: bool = False

    if depth >= 4 and all(map(isliteral, curr.to_list())):
        boom = True
        return True, curr
    else:
        for cp in curr.to_list():
            if ispair(cp):
                boom, ep = explode(cp, depth+1)
                if boom:
                    return boom, ep

    return boom, None


if __name__ == "__main__":
    for l in parse_json("./2021/day18/data/explode_1"):
        p = Pair(l)
        print(p)
        boom, ep = explode(p)
        print(boom, ep)