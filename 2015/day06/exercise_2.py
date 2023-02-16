#!/usr/bin/env python3

"""
--- Part Two ---
You just finish implementing your winning light pattern when you realize you mistranslated Santa's message from Ancient Nordic Elvish.

The light grid you bought actually has individual brightness controls; each light can have a brightness of zero or more. The lights all start at zero.

The phrase turn on actually means that you should increase the brightness of those lights by 1.

The phrase turn off actually means that you should decrease the brightness of those lights by 1, to a minimum of zero.

The phrase toggle actually means that you should increase the brightness of those lights by 2.

What is the total brightness of all lights combined after following Santa's instructions?

For example:

turn on 0,0 through 0,0 would increase the total brightness by 1.
toggle 0,0 through 999,999 would increase the total brightness by 2000000.
"""

from parser import parse_commands

# The phrase turn on actually means that you should increase
# the brightness of those lights by 1.
def turn_on(display, x, y):
    # print("turn on", x, y)
    display[x][y] += 1


# The phrase toggle actually means that you should increase
# the brightness of those lights by 2.
def toggle(display, x, y):
    # print("toggle", x, y)
    display[x][y] += 2


# The phrase turn off actually means that you should decrease
# the brightness of those lights by 1, to a minimum of zero.
def turn_off(display, x, y):
    # print("turn off", x, y)
    if display[x][y] > 0:
        display[x][y] -= 1


commands = {"turn on": turn_on, "toggle": toggle, "turn off": turn_off}


def execute_command(display, cmd):
    x1, y1, x2, y2 = cmd.range()
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            commands[cmd.command](display, x, y)


def count_brightness(display):
    count = 0
    for x in range(len(display)):
        count += sum(y for y in display[x])
    return count


width = 1000
height = 1000
display = [[0 for x in range(width)] for y in range(height)]

for cmd in parse_commands("./data/full"):
    execute_command(display, cmd)

print(count_brightness(display))