#!/usr/bin/env python3

from parser import parse_strs

bits = []
width = 0
init = False

for i, line in enumerate(parse_strs("./2021/day03/data/full")):
    if not init:
        init = True
        width = len(line)
        for j in range(0, width):
            bits.append([0,0])

    for j in range(0, width):
        bits[j][int(line[j])] += 1

# print(bits)

g = int("".join(["0" if bits[i][0] > bits[i][1] else "1" for i in range(0, width)]),2)
e = int("".join(["0" if bits[i][0] <= bits[i][1] else "1" for i in range(0, width)]),2)

print(f"g: {g}, e: {e}, g*e: {g*e}")
    
