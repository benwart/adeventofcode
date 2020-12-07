import re
from collections import namedtuple

rules_regex = re.compile(r"(?P<outer>.*)\s+bags\s+contain\s(?P<inner>.*)\.$")
bag_color_regex = re.compile(r"((?P<count>\d+)\s+)?(?P<color>.*)\s+bag(s)?")
InnerRule = namedtuple("InnerRule", ("count", "color"))


def get_inner_rule(inner):
    match = bag_color_regex.match(inner).groupdict()
    return InnerRule(int(match["count"]), match["color"])


def split_inner_rules(inner_rules):
    output = tuple()
    if not "no other bags" in inner_rules:
        output = tuple(
            map(
                lambda i: get_inner_rule(i),
                inner_rules.split(", "),
            )
        )

    return output


def parse(filepath):
    rules = {}
    with open(filepath) as f:
        for line in f:
            clean = line.rstrip()
            match = rules_regex.match(clean)
            if match:
                groups = match.groupdict()
                outer_bag = groups["outer"]
                inner_bags = split_inner_rules(groups["inner"])
                rules[outer_bag] = inner_bags
            else:
                print(f"No Match found: {clean}")

    return rules
