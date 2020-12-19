#!/usr/bin/env python3

import re
from functools import cache
from parser import parse_data

rules, messages = parse_data("./data/full")

# update rules 8 and 11
# found this on reddit
max_rec = 10
rules[8]["refs"] = "|".join(["42 " * i for i in range(1, max_rec)])
rules[11]["refs"] = "|".join(["42 " * i + "31 " * i for i in range(1, max_rec)])


@cache
def get_ref_rule(ref, id):
    output = []
    for num in ref:
        output.append(get_rule_regex(int(num)) if int(num) != id else "(?R)?")
    return f"(?:{''.join(output)})"


@cache
def get_rule_regex(id):
    rule = rules[id]

    # at the bottom return the literal
    if rule["literal"]:
        return rule["literal"]

    # not there yet...break up and recurse further
    if "|" in rule["refs"]:
        refs = [tuple(ref.strip().split(" ")) for ref in rule["refs"].split("|")]
    else:
        refs = [tuple(rule["refs"].split(" "))]

    return f"(?:{'|'.join(get_ref_rule(tuple(ref), id) for ref in refs)})"


regex_rule_str = get_rule_regex(0)
RULE_0_REGEX = re.compile(f"^{regex_rule_str}$")

count = 0
for msg in messages:
    m = RULE_0_REGEX.match(msg)
    if m:
        count += 1

print(f"Total Matches for Rule 0: {count}")