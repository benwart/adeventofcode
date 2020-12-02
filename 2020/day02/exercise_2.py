#!/usr/bin/env python3

import re

raw_regex = r"^(\d+)-(\d+)\s+([a-zA-Z]):\s+(.*)$"


class Policy:
    def __init__(self, first, second, char):
        self.indices = (int(first), int(second))
        self.char = char

    def __repr__(self):
        return f"Policy(indices:{self.indices}, char:'{self.char}')"


def split_line(line):
    match = re.match(raw_regex, line)

    if match:
        policy = Policy(*match.groups()[0:3])
        password = match.groups()[3]
        return policy, password

    raise ValueError


def validate(policy, password):

    count = 0
    for index in policy.indices:
        # index values are 1 based
        if policy.char == password[index - 1]:
            count += 1

    return count == 1


valid = 0
with open("./passwords") as f:
    for line in f:
        try:
            if validate(*split_line(line)):
                valid += 1
        except Exception as inst:
            print(inst)

print(f"Valid Passwords: {valid}")