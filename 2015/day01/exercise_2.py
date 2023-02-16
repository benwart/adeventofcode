#!/usr/bin/env python3

"""
--- Part Two ---
Now, given the same instructions, find the position of the first character that causes him to enter the basement (floor -1). The first character in the instructions has position 1, the second character has position 2, and so on.

For example:

) causes him to enter the basement at character position 1.
()()) causes him to enter the basement at character position 5.
What is the position of the character that causes Santa to first enter the basement?
"""

from parser import chars


movement = {
    "(": 1,
    ")": -1,
}

floor = 0

for i, c in enumerate(chars("./data/full", 1)):
    floor += movement[c]
    if floor < 0:
        break

print(f"Position of 1st -1 Floor: {i + 1}")