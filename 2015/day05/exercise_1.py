"""
--- Day 5: Doesn't He Have Intern-Elves For This? ---
Santa needs help figuring out which strings in his text file are naughty or nice.

A nice string is one with all of the following properties:

It contains at least three vowels (aeiou only), like aei, xazegov, or aeiouaeiouaeiou.
It contains at least one letter that appears twice in a row, like xx, abcdde (dd), or aabbccdd (aa, bb, cc, or dd).
It does not contain the strings ab, cd, pq, or xy, even if they are part of one of the other requirements.

For example:

ugknbfddgicrmopn is nice because it has at least three vowels (u...i...o...), a double letter (...dd...), and none of the disallowed substrings.
aaa is nice because it has at least three vowels and a double letter, even though the letters used by different rules overlap.
jchzalrnumimnmhp is naughty because it has no double letter.
haegwjzuvuyypxyu is naughty because it contains the string xy.
dvszwmarrgswjxmb is naughty because it contains only one vowel.

How many strings are nice?
"""
import re
from itertools import groupby
from parser import parse_strs

VOWELS_REGEX = re.compile(r"([aeiou][^aeiou]*?){3,}?")
DOUBLE_REGEX = re.compile(r"([a-z])\1")
INVALID_REGEX = re.compile(r"(ab|cd|pq|xy)")


def checks(s):
    vowels = VOWELS_REGEX.findall(s)
    double = DOUBLE_REGEX.findall(s)
    invalid = INVALID_REGEX.findall(s)

    output = [
        {"s": s, "matches": vowels, "result": len(vowels) > 0},
        {"s": s, "matches": double, "result": len(double) > 0},
        {"s": s, "matches": invalid, "result": len(invalid) == 0},
    ]
    return output


def is_nice(s: str):
    return all(map(lambda c: c["result"], checks(s)))


naughty_or_nice = [is_nice(s) for s in parse_strs("./data/full")]
# print(naughty_or_nice)

naughty = [n for n in filter(lambda x: not x, naughty_or_nice)]
nice = [n for n in filter(lambda x: x, naughty_or_nice)]

print(f"Naughty: {len(naughty)}, Nice: {len(nice)}")