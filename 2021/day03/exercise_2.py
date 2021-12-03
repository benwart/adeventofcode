#!/usr/bin/env python3

import operator

from parser import parse_strs


def count_bit(values, bit, op):
    count = [0,0]
    
    for value in values:
        count[int(value[bit])] += 1

    return 1 if op(count[1], count[0]) else 0


def filter_values(values, op):
    filtered = list(values)
    i = 0
    while len(filtered) > 1:
        m = count_bit(filtered, i, op)
        filtered = [v for v in filtered if int(v[i]) == m]
        i += 1

        # print(filtered)

    return int(filtered[0], 2)


values = list(parse_strs("./2021/day03/data/full"))

o2 = filter_values(values, operator.ge)
co2 = filter_values(values, operator.lt)

print(f"o2: {o2}, co2: {co2}, answer: {o2 * co2}")


    
