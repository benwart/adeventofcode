#!/usr/bin/env python3

from collections import namedtuple

Input = namedtuple("Input", "value, answer")

example1 = Input("389125467", "67384529")
full = Input("974618352", None)

str_cup = lambda curr, i, cup: f"({str(cup)})" if curr == i else str(cup)

cups = [int(cup) for cup in full.value]
curr = 0
for move in range(1, 100 + 1):
    print(f"-- move {move} --")
    print(f"cups: {' '.join([str_cup(curr, i, cup) for i, cup in enumerate(cups)])}")

    # pickup 3 cups
    pickup = []
    for p in range(3):
        i = (curr + 1) % len(cups)
        if i < curr:
            curr -= 1
        pickup.append(cups.pop(i))
    print(f"pick up: {' '.join([str(cup) for cup in pickup])}")

    # select next cup\
    dest = None
    look = cups[curr]
    l = len(example1.value) + 1
    while dest == None:
        look = (l + look - 1) % l
        if look in cups:
            dest = cups.index(look)

    print(f"destination: {cups[dest]}")

    # insert picked up cups
    cups[dest + 1 : dest + 1] = pickup

    # update curr
    if dest < curr:
        curr += 3

    curr = (curr + 1) % len(cups)
    print("")

print("-- finial --")
print(f"cups: {' '.join([str_cup(curr, i, cup) for i, cup in enumerate(cups)])}")

# shift cups to get answer
start = cups.index(1)
print("".join(str(cups[i % len(cups)]) for i in range(start + 1, start + len(cups))))
