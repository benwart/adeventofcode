#!/usr/bin/env python3

from parser import parse_fish_ages

data = parse_fish_ages("./2021/day06/data/full")

days = 80

# print(f"Initial State: {','.join(map(str, data))}")

for day in range(1,days + 1):

    add = 0

    for i, fish in enumerate(data):

        if fish > 0:
            # reduce age of all fish greater than 0
            data[i] -= 1
        else:
            # reset 0 to 6
            data[i] = 6

            # remember to add new fish
            add += 1 

    # add new fish the the end of the array
    data.extend([8 for i in range(add)])

    # print results at the end of each day
    # print(f"After Day {day:2}: {','.join(map(str, data))}")

print(f"Total Fish: {len(data)}")