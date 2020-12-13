#!/usr/bin/env python3

import math
from collections import namedtuple
from parser import parse_scedule_exercise2

Combined = namedtuple("Combined", ("n", "r"))
bus_ids = parse_scedule_exercise2("./data/full")

# example

# 0 = x % 7
# 1 = x % 13
# 4 = x % 59
# 6 = x % 31
# 7 = x % 19

# x = 1068781

#########################################################
# chinese remainder (faster)
#########################################################
from functools import reduce
from typing import Iterable


def chinese_remainder(n: Iterable[int], a: Iterable[int]):
    sum = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a: int, b: int):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


n = [id for i, id in enumerate(bus_ids) if id != "x"]
a = [((id - i) % id) for i, id in enumerate(bus_ids) if id != "x"]

result = int(chinese_remainder(n, a))

print(f"Random: {result}")

#############################
# off reddit
#############################
import functools
import operator

busses = [
    Combined(bus, (bus - i) % bus) for i, bus in enumerate(bus_ids) if not "x" == bus
]

product = functools.reduce(operator.mul, [n for n, r in busses], 1)
B = [product // n for n, r in busses]
x = [pow(B[i], -1, busses[i].n) for i in range(len(B))]
sum_list = [B[i] * x[i] * busses[i][1] for i in range(len(B))]
sum_value = sum(sum_list)

print(f"Reddit: {sum_value % product}")
