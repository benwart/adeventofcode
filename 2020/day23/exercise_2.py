#!/usr/bin/env python3

import progressbar
from collections import namedtuple
from math import prod

Input = namedtuple("Input", "value, answer")

example1 = Input("389125467", "67384529")
full = Input("974618352", None)

str_cup = lambda curr, i, cup: f"({str(cup)})" if curr == i else str(cup)

cups = [int(cup) for cup in example1.value]
cups.extend([i for i in range(max(cups) + 1, 1000000 + 1)])
# stop = 10000000 + 1
stop = 1000 + 1

with progressbar.ProgressBar(max_value=stop) as bar:
    curr = 0
    max_value = 1000000 + 1
    for move in range(1, stop):

        # pickup 3 cups
        pickup = []
        for p in range(3):
            i = (curr + 1) % len(cups)
            if i < curr:
                curr -= 1
            pickup.append(cups.pop(i))

        # select next cup\
        dest = None
        look = cups[curr]

        while dest == None:
            look = (max_value + look - 1) % max_value
            if look not in pickup and look != 0:
                dest = cups.index(look)

        # insert picked up cups
        cups[dest + 1 : dest + 1] = pickup

        # update curr
        if dest < curr:
            curr += 3

        curr = (curr + 1) % len(cups)

        bar.update(move)

# shift cups to get answer
start = cups.index(1)
print(prod(cups[i % len(cups)] for i in range(start + 1, start + 3)))
