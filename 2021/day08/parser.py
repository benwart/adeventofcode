#!/usr/bin/env python3

def parse_strs(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


def parse_data(filepath):
    for line in parse_strs(filepath):
        # split input | output
        in_out = line.split("|")

        # split input
        input = [i for i in map(lambda x: x.strip(), in_out[0].split(" ")) if len(i) > 0]
        output = [i for i in map(lambda x: x.strip(), in_out[1].split(" ")) if len(i) > 0]

        yield input, output

if __name__ == "__main__":
    for input, output in parse_data("./2021/day08/data/example_1"):
        print(f"{input} | {output}")
