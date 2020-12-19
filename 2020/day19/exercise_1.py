#!/usr/bin/env python3

import re
from functools import cache
from parser import parse_data

rules, messages = parse_data("./data/full")


@cache
def get_ref_rule(ref):
    return "".join(get_rule_regex(int(id)) for id in ref)


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

    return f"(?:{'|'.join(get_ref_rule(tuple(ref)) for ref in refs)})"


RULE_0_REGEX = re.compile(f"^{get_rule_regex(0)}$")

count = 0
for msg in messages:
    m = RULE_0_REGEX.match(msg)
    if m:
        count += 1

print(f"Total Matches for Rule 0: {count}")