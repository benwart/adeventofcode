#!/usr/bin/env python3

from parser import parse_program


def set_bit(k, n):
    output = (1 << k) | n
    # print(f"{format(n,'#010b')}")
    # print(f"{format(output,'#010b')}")
    return output


def unset_bit(k, n):
    output = n & ~(1 << k)
    # print(f"{format(n,'#010b')}")
    # print(f"{format(output,'#010b')}")
    return output


operation = {
    "1": set_bit,
    "0": unset_bit,
}


def apply_mask(n, mask):
    output = n
    for k, bit in ((k, bit) for k, bit in enumerate(reversed(mask)) if bit != "X"):
        output = operation[bit](k, output)
    return output


memory = {}
for line in parse_program("./data/full"):
    masked = apply_mask(n=line["value"], mask=line["mask"])
    memory[line["address"]] = masked
    # print(
    #     f"input: {format(line['value'], '#010b')}, masked: {masked} ({format(masked, '#010b')})"
    # )

total = sum(memory.values())
print(f"Total: {total}")