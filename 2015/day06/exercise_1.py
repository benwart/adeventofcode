#!/usr/bin/env python3

"""
--- Day 6: Probably a Fire Hazard ---
Because your neighbors keep defeating you in the holiday house decorating contest year after year, you've decided to deploy one million lights in a 1000x1000 grid.

Furthermore, because you've been especially nice this year, Santa has mailed you instructions on how to display the ideal lighting configuration.

Lights in your grid are numbered from 0 to 999 in each direction; the lights at each corner are at 0,0, 0,999, 999,999, and 999,0. The instructions include whether to turn on, turn off, or toggle various inclusive ranges given as coordinate pairs. Each coordinate pair represents opposite corners of a rectangle, inclusive; a coordinate pair like 0,0 through 2,2 therefore refers to 9 lights in a 3x3 square. The lights all start turned off.

To defeat your neighbors this year, all you have to do is set up your lights by doing the instructions Santa sent you in order.

For example:

turn on 0,0 through 999,999 would turn on (or leave on) every light.
toggle 0,0 through 999,0 would toggle the first line of 1000 lights, turning off the ones that were on, and turning on the ones that were off.
turn off 499,499 through 500,500 would turn off (or leave off) the middle four lights.

After following the instructions, how many lights are lit?
"""

from parser import parse_commands


def turn_on(display, x, y):
    # print("turn on", x, y)
    return True


def toggle(display, x, y):
    # print("toggle", x, y)
    return not display[x][y]


def turn_off(display, x, y):
    # print("turn off", x, y)
    return False


commands = {"turn on": turn_on, "toggle": toggle, "turn off": turn_off}


def execute_command(display, cmd):
    x1, y1, x2, y2 = cmd.range()
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            display[x][y] = commands[cmd.command](display, x, y)


def count_on(display):
    count = 0
    for x in range(len(display)):
        count += len([y for y in display[x] if y])
    return count


width = 1000
height = 1000
display = [[False for x in range(width)] for y in range(height)]

for cmd in parse_commands("./data/full"):
    execute_command(display, cmd)

print(count_on(display))