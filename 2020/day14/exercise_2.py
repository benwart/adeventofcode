#!/usr/bin/env python3

from collections import deque
from parser import parse_program


def set_bit(k, n):
    output = (1 << k) | n
    return output


def unset_bit(k, n):
    output = n & ~(1 << k)
    return output


def recurse_floating_bits(output, value, mask):

    jobs = deque()
    jobs.append((value, -1))

    while len(jobs) > 0:

        v, i = jobs.pop()

        # pick the first X (k)
        #  from start
        index = None
        for k, bit in (
            (k, bit) for k, bit in enumerate(reversed(mask)) if k > i and bit == "X"
        ):
            index = k
            # print(index)
            break

        if index == None:
            continue

        # unset k
        v = unset_bit(index, v)

        # append to output
        output.add(v)

        # store job
        jobs.append((v, index))

        # set k
        v = set_bit(index, v)

        # append to output
        output.add(v)

        # recurse
        jobs.append((v, index))


def apply_mask(address, mask):
    masked = address

    # handle setting static bits
    for k, bit in (
        (k, bit) for k, bit in enumerate(reversed(mask)) if bit not in ("X", "0")
    ):
        masked = set_bit(k, masked)

    # handle floating bits
    output = set()
    recurse_floating_bits(output, masked, mask)

    return output


memory = {}
for line in parse_program("./data/full"):
    addresses = apply_mask(address=line["address"], mask=line["mask"])
    for address in addresses:
        memory[address] = line["value"]

total = sum(memory.values())
print(f"Total: {total}")