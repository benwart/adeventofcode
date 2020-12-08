#!/usr/bin/env python3

"""
--- Part Two ---
The next year, to speed up the process, Santa creates a robot version of himself, Robo-Santa, to deliver presents with him.

Santa and Robo-Santa start at the same location (delivering two presents to the same starting house), then take turns moving based on instructions from the elf, who is eggnoggedly reading from the same script as the previous year.

This year, how many houses receive at least one present?

For example:

^v delivers presents to 3 houses, because Santa goes north, and then Robo-Santa goes south.
^>v< now delivers presents to 3 houses, and Santa and Robo-Santa end up back where they started.
^v^v^v^v^v now delivers presents to 11 houses, with Santa going one direction and Robo-Santa going the other.
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


santa = Position(x=0, y=0)
robo = Position(x=0, y=0)

locations = set()
locations.add(str(santa))


def update_position(p, d):
    u = p.apply_direction(d)
    if str(u) not in locations:
        locations.add(str(u))
    return u


for i, d in enumerate(parse_directions("./data/full", 1)):
    if i % 2 == 0 or i == 0:
        santa = update_position(santa, d)
    else:
        robo = update_position(robo, d)

print(len(locations))