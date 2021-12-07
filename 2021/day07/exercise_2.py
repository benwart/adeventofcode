#!/usr/bin/env python3

from functools import cache
from parser import parse_ints

@cache
def move_cost(distance):
    cost = 0
    for i in range(0, distance + 1):
        cost += i
    
    return cost


def fuel_cost(crabs, destination):
    return sum(
        map(
            lambda c: move_cost(abs(c - destination)), 
            crabs
        )
    )


def min_cost(crabs, rng):
    return min(
        map(lambda t: {"index": t[0], "cost": t[1]}, 
            enumerate(
                map(lambda d: fuel_cost(crabs, d), rng)
            )
        ),
        key=lambda i: i["cost"]
    )

crabs = parse_ints("./2021/day07/data/full")
min_crab = min(crabs)
max_crab = max(crabs)

print(min_cost(crabs, range(min_crab, max_crab+1)))
