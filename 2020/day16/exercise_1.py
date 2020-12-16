#!/usr/bin/env python3

from functools import reduce
from parser import parse_data

data = parse_data("./data/full")

# generate list with True/False for valid values
rules = reduce(lambda acc, rs: acc + rs, data["fields"].values(), [])

# print(rules)

minimum = min(v for r in rules for v in r)
maximum = max(v for r in rules for v in r)

# print(minimum, maximum)

offset = minimum
valid = [
    any(map(lambda r: r[0] <= i and r[1] >= i, rules))
    for i in range(minimum, maximum + 1)
]

invalid = 0
for ticket in data["nearby"]:
    for num in ticket:
        if num < minimum or num > maximum or not valid[num - offset]:
            invalid += num

print(f"Sum of Invalid: {invalid}")
