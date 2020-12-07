#!/usr/bin/env python3

"""
--- Part Two ---
It's getting pretty expensive to fly these days - not because of ticket prices, but because of the ridiculous number of bags you need to buy!

Consider again your shiny gold bag and the rules from the above example:

faded blue bags contain 0 other bags.
dotted black bags contain 0 other bags.
vibrant plum bags contain 11 other bags: 5 faded blue bags and 6 dotted black bags.
dark olive bags contain 7 other bags: 3 faded blue bags and 4 dotted black bags.

So, a single shiny gold bag must contain 1 dark olive bag (and the 7 bags within it) plus 2 vibrant plum bags (and the 11 bags within each of those): 1 + 1*7 + 2 + 2*11 = 32 bags!

Of course, the actual rules have a small chance of going several levels deeper than this example; be sure to count all of the bags, even if the nesting becomes topologically impractical!

Here's another example:

shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.

In this example, a single shiny gold bag must contain 126 other bags.

How many individual bags are required inside your single shiny gold bag?
"""

import re
from collections import namedtuple
from functools import cache

rules_regex = re.compile(r"(?P<outer>.*)\s+bags\s+contain\s(?P<inner>.*)\.$")
bag_color_regex = re.compile(r"((?P<count>\d+)\s+)?(?P<color>.*)\s+bag(s)?")
Rule = namedtuple("Rule", ("key", "inner"))
InnerRule = namedtuple("InnerRule", ("count", "color"))


def get_inner_rule(inner):
    match = bag_color_regex.match(inner).groupdict()
    return InnerRule(int(match["count"]), match["color"])


def split_inner_rules(inner_rules):
    inner_rules = tuple()
    if not "no other bags" in groups["inner"]:
        inner_rules = tuple(
            map(
                lambda i: get_inner_rule(i),
                groups["inner"].split(", "),
            )
        )

    return inner_rules


rules = {}

with open("./data/full") as f:
    for line in f:
        match = rules_regex.match(line.rstrip())
        if match:
            groups = match.groupdict()
            outer_bag = groups["outer"]
            inner_bags = split_inner_rules(groups["inner"])
            rules[outer_bag] = inner_bags
        else:
            print(f"No Match found: {line.rstrip()}")


@cache
def recurse_count(key, inner_rules):
    # print(f"{key} with {inner_rules}")
    count = 1
    for inner in inner_rules:
        count += inner.count * recurse_count(inner.color, rules[inner.color])
    return count


# print(rules)

shiny_gold = ("shiny_gold", rules["shiny gold"])
count = recurse_count(*shiny_gold)

print(count - 1)
