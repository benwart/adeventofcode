#!/usr/bin/env python3

"""
"""

from hashlib import sha256
from parser import parse_directions


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        h = (self.y << 16) ^ self.x
        return h

    def __repr__(self):
        return f"{self.x},{self.y}"

    def apply_direction(self, d):
        return Position(self.x + d.x, self.y + d.y)


p = Position(x=0, y=0)
locations = {}
locations[str(p)] = p

for d in parse_directions("./data/full", 1):
    p = p.apply_direction(d)
    if str(p) not in locations:
        locations[str(p)] = p

print(len(locations))