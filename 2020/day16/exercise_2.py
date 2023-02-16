#!/usr/bin/env python3

import numpy as np

from functools import reduce
from math import prod
from parser import parse_data

data = parse_data("./data/full")
rules = reduce(lambda acc, rs: acc + rs, data["fields"].values(), [])
minimum = min(v for r in rules for v in r)
maximum = max(v for r in rules for v in r)
lookup = [
    any(map(lambda r: r[0] <= i and r[1] >= i, rules))
    for i in range(minimum, maximum + 1)
]


def is_valid(lookup, ticket):
    for num in ticket:
        if num < minimum or num > maximum or not lookup[num - minimum]:
            return False
    return True


def valid_nearby(data):
    return [t for t in data["nearby"] if is_valid(lookup, t)]


def valid_field_col(rules, col):
    [a, b] = rules
    check = lambda v: (a[0] <= v and a[1] >= v) or (b[0] <= v and b[1] >= v)
    return all(check(v) for v in col)


nearby = np.array(valid_nearby(data), dtype=np.int16)

# find all the columns that match each rule
possible = {}
mapping = {}
for name, rules in data["fields"].items():
    possible[name] = [
        c for c in range(nearby.shape[1]) if valid_field_col(rules, nearby[:, c])
    ]

# repeat until we have only 1 column for each field
while any(map(lambda v: len(v) >= 1, possible.values())):

    # find smallest field of possible columns
    min_field, columns = min(possible.items(), key=lambda f: len(f[1]))
    if len(columns) > 1:
        print("no solution...more than 1 possible col for minimum field")
        break

    col_to_remove = columns[0]

    # add to mapping and remove from possible
    mapping[min_field] = col_to_remove
    del possible[min_field]

    # remove that column from other fields
    for name in (k for k in possible):
        possible[name]
        if col_to_remove in possible[name]:
            possible[name].remove(col_to_remove)

# get all the departure fields from out ticket
departures = [v for k, v in mapping.items() if k.startswith("departure")]
solution = prod(v for i, v in enumerate(data["ticket"]) if i in departures)

print(f"Product of Departure Fields from my Ticket: {solution}")
