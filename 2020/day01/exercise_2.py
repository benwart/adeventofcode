#!/usr/bin/env python3

"""
--- Part Two ---
The Elves in accounting are thankful for your help; one of them even offers you a starfish coin 
they had left over from a past vacation. They offer you a second one if you can find three numbers 
in your expense report that meet the same criteria.

Using the above example again, the three entries that sum to 2020 are 979, 366, and 675. 
Multiplying them together produces the answer, 241861950.

In your expense report, what is the product of the three entries that sum to 2020?
"""

import bisect
import math
import sys

from pprint import pprint


def insert(list, n):
    bisect.insort(list, n)
    return list


expenses = []

with open("./data") as f:
    for line in f:
        insert(expenses, int(line))

print(expenses)


def check_sum(arr, n, *args):
    for i in range(len(args), len(arr) - len(args)):
        if n - 1 > len(args):
            if check_sum(arr, n, arr[i], *args):
                return True
        else:
            check = sum(args) + arr[i]
            if check < 2020:
                print(".", end="")
            if check == 2020:
                print(f"*\nAnswer is: {math.prod([arr[i], *args])}")
                return True
            if check > 2020:
                print(">")
                break

    # didn't find a match
    return False


check_sum(expenses, 3)
