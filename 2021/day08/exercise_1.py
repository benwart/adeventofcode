#!/usr/bin/env python3

from parser import parse_data

unique_lengths = set([2, 4, 3, 7])

count = 0
for input, output in parse_data("./2021/day08/data/full"):
    # count the occurances of 1, 4, 7, 8 in output
    for n in output:
        count += 1 if len(n) in unique_lengths else 0 

print(count)
