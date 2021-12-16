#!/usr/bin/env python3

from collections import defaultdict
from parser import parse_data


def get_pairs(template):
    pairs = defaultdict(lambda:0)

    # generate list of pairs from template
    for i in range(0, len(template)-1):
        pairs[template[i:i+2]] += 1

    return pairs


def get_elements(template):
    elements = defaultdict(lambda: 0)
    for e in template:
        elements[e] += 1

    return elements


def iteration(insertions, pairs, elements):
    out_pairs = defaultdict(lambda: 0)
    out_elements = defaultdict(lambda: 0, elements)

    for pair, count in pairs.items():
        # insertion
        insert = insertions[pair]
        out_elements[insert] += count

        # create new pairs based on insertion
        p0 = f"{pair[0]}{insert}"
        p1 = f"{insert}{pair[1]}"

        # set new pairs count to count
        out_pairs[p0] += count
        out_pairs[p1] += count

    return out_pairs, out_elements


def main():
    template, insertions = parse_data("./2021/day14/data/full")

    steps = 40

    print(f"Template: {template}")

    # get pairs and store them in the state
    pairs = get_pairs(template)
    elements = get_elements(template)

    for _ in range(1, steps+1):
        pairs, elements = iteration(insertions, pairs, elements)

    sorted_elements = sorted(elements.items(), key=lambda t: t[1])

    # print(sorted_elements)

    min_element = sorted_elements[0]
    max_element = sorted_elements[-1]

    print(f"min: {min_element}")
    print(f"max: {max_element}")
    print(f"delta: {max_element[1] - min_element[1]}")


if __name__ == "__main__":
    main()
