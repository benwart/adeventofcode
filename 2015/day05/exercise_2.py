"""
--- Part Two ---
Realizing the error of his ways, Santa has switched to a better model of determining whether a string is naughty or nice. None of the old rules apply, as they are all clearly ridiculous.

Now, a nice string is one with all of the following properties:

It contains a pair of any two letters that appears at least twice in the string without overlapping, like xyxy (xy) or aabcdefgaa (aa), but not like aaa (aa, but it overlaps).
It contains at least one letter which repeats with exactly one letter between them, like xyx, abcdefeghi (efe), or even aaa.

For example:

qjhvhtzxzqqjkmpb is nice because is has a pair that appears twice (qj) and a letter that repeats with exactly one letter between them (zxz).
xxyxx is nice because it has a pair that appears twice and a letter that repeats with one between, even though the letters used by each rule overlap.
uurcxstgmygtbstg is naughty because it has a pair (tg) but no repeat with a single letter between them.
ieodomkazucvgmuy is naughty because it has a repeating letter with one between (odo), but no pair that appears twice.

How many strings are nice under these new rules?
"""

import re
from itertools import groupby
from parser import parse_strs

PAIRS_REGEX = re.compile(r"([a-z]{2}).*?\1")
DOUBLE_REGEX = re.compile(r"([a-z]).\1")


def checks(s):
    pairs = PAIRS_REGEX.findall(s)
    double = DOUBLE_REGEX.findall(s)

    output = [
        {"s": s, "matches": pairs, "result": len(pairs) > 0},
        {"s": s, "matches": double, "result": len(double) > 0},
    ]
    return output


def is_nice(s: str):
    return all(map(lambda c: c["result"], checks(s)))


naughty_or_nice = [is_nice(s) for s in parse_strs("./data/full")]
# print(naughty_or_nice)

naughty = [n for n in filter(lambda x: not x, naughty_or_nice)]
nice = [n for n in filter(lambda x: x, naughty_or_nice)]

print(f"Naughty: {len(naughty)}, Nice: {len(nice)}")