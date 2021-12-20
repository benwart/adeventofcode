#!/usr/bin/env python3

from copy import deepcopy
from math import floor, ceil
from parser import parse_number, Number


def print_n(n: Number):
    output = []
    for i, v in enumerate(n):
        output.append(str(v))
        if i < len(n)-1:
            if isinstance(v, int) and \
               ( \
                   isinstance(n[i+1], int) or \
                   n[i+1] == "["
               ):
                output.append(",")
            elif v == "]" and n[i+1] == "[":
                output.append(",")
    
    print("".join(output))


depth_modifier = {
    "[": 1,
    "]": -1,
}

def explode_left(n: Number, i: int):
    # capture n[i] to add to left
    v = n[i]

    # work left until we find a number
    for j in range(i-1, 0, -1):
        if isinstance(n[j], int):
            n[j] += v
            break


def explode_right(n: Number, i: int):
    # capture n[i] to add to left
    v = n[i]

    # work left until we find a number
    for j in range(i+1, len(n), 1):
        if isinstance(n[j], int):
            n[j] += v
            break


def explode(n: Number) -> bool:
    """
    1. left value is added to the first number on the left (if any)
    2. right value is added to the first number on the right (if any)
    3. replace the pair with 0
    """
    result = False
    length = len(n)
    depth = 0
    for i, v in enumerate(n):
        if isinstance(v, str):
            depth += depth_modifier[v]
        elif depth > 4 and isinstance(v, int) and i < length-1 and isinstance(n[i+1], int):

            # found pair to be exploded
            result = True
            explode_left(n, i)
            explode_right(n, i+1)

            # replace pair with 0
            # all pairs are "[", i, i+1, "]"
            start = i-1
            end = i+2
            del n[start:end+1]
            n.insert(start, 0)
            break

    return result


def split_int(i: int) -> Number:
    """
    Divide by 2 and floor value in left and ceil value in right.
    """
    s = i/2.0
    return ["[", int(floor(s)), int(ceil(s)), "]"]
    

def split(n: Number) -> bool:
    """
    To split a regular number, replace it with a pair; the left element of the 
    pair should be the regular number divided by two and rounded down, while the
    right element of the pair should be the regular number divided by two and 
    rounded up. 
    
    For example:
    - 10 becomes `[5,5]`
    - 11 becomes `[5,6]`
    - 12 becomes `[6,6]`
    """

    result: bool = False

    # find leftmost number >= 10 and split the int
    for i, v in enumerate(n):
        if isinstance(v, int) and v >= 10:
            result = True

            s = split_int(v)
            del n[i]

            for c in reversed(s):
                n.insert(i, c)
                
            break

    return result


reductions = [
    explode,
    split,
]

def reduce(n: Number) -> Number:
    """
    1. If any pair is nested inside four pairs, the leftmost such pair explodes.
    2. If any regular number is 10 or greater, the leftmost such regular number splits.
    3. Once no action in the above list applies, the snailfish number is reduced.
    """

    result = True

    # keep going until reductions all return false
    while result:
        # print_n(n)
        for r in reductions:
            result = r(n)
            
            # stop this round if reduction succeeds
            if result:
                break

    # return current state of n
    return n


def add(n1: Number, n2: Number) -> Number:

    sum = ["["]
    sum += deepcopy(n1)
    sum += deepcopy(n2)
    sum += ["]"]

    # print("  ", end="")
    # print_n(n1)
    # print(" + ", end="")
    # print_n(n2)
    # print(" = ", end="")
    reduce(sum)
    
    return sum


def magnitude(n: Number) -> int:
    while len(n) > 1:
        # find a pair and calculate magnitude
        for i, v in enumerate(n):
            if isinstance(v, int) and i < len(n)-1 and isinstance(n[i+1], int):
                l, r = v, n[i+1]
                m = (3 * l) + (2 * r) 

                # remove pair from n
                del n[i-1:i+3]

                # replace with magnitude
                n.insert(i-1, m)

    return n[0]


def add_magnitude(n1: Number, n2: Number) -> tuple[Number, int]:
    s = add(n1, n2)
    m = magnitude(s)
    return s, m


if __name__ == "__main__":
    magnitudes = []
    numbers = list(parse_number("./2021/day18/data/full"))

    for i, n in enumerate(numbers):
        for j, m in enumerate(numbers):
            if i == j:
                continue

            magnitudes.append(magnitude(add(n, m)))

    print(f"magnitude: {max(magnitudes)}")
