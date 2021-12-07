#!/usr/bin/env python3

from parser import parse_ints


def fuel_cost(crabs, destination):
    return sum(map(lambda c: abs(c - destination), crabs))


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
