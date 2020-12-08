#!/usr/bin/env python2

import re

INSTRUCTION_REGEX = re.compile(r"(?P<op>nop|acc|jmp)\s+(?P<value>[+-]\d+)")


def parse(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


def instructions(filepath):
    for line in parse(filepath):
        m = INSTRUCTION_REGEX.match(line).groupdict()
        yield {
            "op": m["op"],
            "value": int(m["value"]),
        }
