#!/usr/bin/python3

"""
--- Part Two ---
The final step in breaking the XMAS encryption relies on the invalid number you just found: you must find a contiguous set of at least two numbers in your list which sum to the invalid number from step 1.

Again consider the above example:

35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576

In this list, adding up all of the numbers from 15 through 40 produces the invalid number from step 1, 127. (Of course, the contiguous set of numbers in your actual list might be much longer.)

To find the encryption weakness, add together the smallest and largest number in this contiguous range; in this example, these are 15 and 47, producing 62.

What is the encryption weakness in your XMAS-encrypted list of numbers?
"""

from collections import namedtuple
from parser import parse_ints
from typing import Iterable

data = [i for i in parse_ints("./data/full")]


def check(data: Iterable[int], value: int) -> bool:
    for a in range(0, len(data) - 1):
        for b in range(1, len(data)):
            # print(f"{data[a]} + {data[b]}")
            if data[a] + data[b] == value:
                return True
    return False


def find_number(data: Iterable[int], preamble: int = 25):
    for i in range(preamble, len(data)):
        c = check(data[i - preamble : i + preamble], data[i])
        if not c:
            return data[i]
    return None


num = find_number(data, 25)
print(f"Number: {num}")

start = 0
finish = 0
acc = 0

while finish < len(data):

    if acc < num:
        curr = data[finish]
        acc += curr
        finish += 1

    elif acc > num:
        acc -= data[start]
        start += 1

    elif acc == num:
        subset = data[start:finish]
        minimum = min(subset)
        maximum = max(subset)
        print(f"Weakness: {minimum + maximum}")
        break
