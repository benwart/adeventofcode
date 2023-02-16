#!/usr/bin/env python3

def parse_strs(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


def parse_msg(filepath):
    h = next(parse_strs(filepath))
    print(f"Hex Input: {h}")

    v = list()
    for c in h:
        v.append(f"{bin(int(c, base=16))[2:].zfill(4)}")

    return "".join(v)


if __name__ == "__main__":
    print(parse_msg("./2021/day16/data/example_08"))
