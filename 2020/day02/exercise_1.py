#!/usr/bin/env python3

import re

raw_regex = r"^(\d+)-(\d+)\s+([a-zA-Z]):\s+(.*)$"


class Policy:
    def __init__(self, minimum, maximum, char):
        self.minimum = int(minimum)
        self.maximum = int(maximum)
        self.char = char

    def __repr__(self):
        return f"Policy(minimum:{self.minimum}, maximum:{self.maximum}, char:'{self.char}')"


def split_line(line):
    match = re.match(raw_regex, line)

    if match:
        policy = Policy(*match.groups()[0:3])
        print(policy)
        password = match.groups()[3]
        return policy, password

    raise ValueError


def validate(policy, password):
    count = password.count(policy.char)
    return count >= policy.minimum and count <= policy.maximum


valid = 0
with open("./passwords") as f:
    for line in f:
        try:
            if validate(*split_line(line)):
                valid += 1
        except Exception as inst:
            print(inst)

print(f"Valid Passwords: {valid}")