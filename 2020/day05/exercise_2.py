#!/usr/bin/env python3

"""
--- Part Two ---
Ding! The "fasten seat belt" signs have turned on. Time to find your seat.

It's a completely full flight, so your seat should be the only missing boarding pass in your list. However, there's a catch: some of the seats at the very front and back of the plane don't exist on this aircraft, so they'll be missing from your list as well.

Your seat wasn't at the very front or back, though; the seats with IDs +1 and -1 from yours will be in your list.

What is the ID of your seat?
"""

import bisect
import math


def ordered_insert(list, n):
    bisect.insort(list, n)


replacements = {
    "F": "0",
    "B": "1",
    "L": "0",
    "R": "1",
}

seats = []

with open("./data/full") as f:
    for line in f:
        # split rows and cols, convert to 0/1 string, convert to int type
        row = int("".join(map(lambda x: replacements[x], line[0:7])), 2)
        col = int("".join(map(lambda x: replacements[x], line[7:10])), 2)

        # generate seat id
        id = row * 8 + col

        # do an ordered insert to get a sorted list
        ordered_insert(seats, id)

print(seats)

# iterate through list and look for the first seat that is exactly
# -2 from the next seat
for id in range(0, len(seats) - 1):
    if seats[id] + 2 == seats[id + 1]:
        print(f"Missing Seat ID: {seats[id]+1}")
