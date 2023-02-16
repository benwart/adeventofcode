#!/usr/bin/env python3

import copy
import sys
from enum import Enum
from parser import Location
from parser import parse_locations


def do_lookup(t, w, x, y):
    if x < 0 or y < 0:
        raise IndexError()

    return 1 if t[(y * w) + x] == SeatStatus.TAKEN else 0


class SeatStatus(Enum):
    TAKEN = 0
    EMPTY = 1
    FLOOR = 2


def check_seat(t, w, i):
    x = i % w
    y = (i - x) // w

    left = x == 0
    right = x == w - 1
    top = y == 0
    bottom = y == (len(t) // w) - 1

    # build list of adjacent seats
    adjacent = {
        "top-left": do_lookup(t, w, x - 1, y - 1) if not top and not left else 0,
        "top-middle": do_lookup(t, w, x, y - 1) if not top else 0,
        "top-right": do_lookup(t, w, x + 1, y - 1) if not top and not right else 0,
        "middle-left": do_lookup(t, w, x - 1, y) if not left else 0,
        "middle-right": do_lookup(t, w, x + 1, y) if not right else 0,
        "bottom-left": do_lookup(t, w, x - 1, y + 1) if not bottom and not left else 0,
        "bottom-middle": do_lookup(t, w, x, y + 1) if not bottom else 0,
        "bottom-right": do_lookup(t, w, x + 1, y + 1)
        if not bottom and not right
        else 0,
    }

    # check how many are taken around this location
    occupied = sum(adjacent.values())
    return occupied


taken_map = {
    SeatStatus.TAKEN: "#",
    SeatStatus.EMPTY: "L",
    SeatStatus.FLOOR: ".",
}


def render_plane(t, w, iteration, mapping=None):
    with open(f"./output/{iteration}", "w") as f:
        for i in range(0, len(t), w):
            f.write(
                "".join(
                    map(
                        lambda s: mapping[s] if mapping else f"{s}",
                        [seat for seat in t[i : i + w]],
                    )
                )
            )
            f.write("\n")
        f.flush()


if __name__ == "__main__":

    data = [row for row in parse_locations("./data/full")]
    width = len(data[0])

    flat = [loc for row in data for loc in row]

    neighbors = [0 for loc in flat]
    taken = copy.deepcopy(flat)
    for seat in (i for i, loc in enumerate(flat)):
        if taken[seat] == Location.SEAT:
            taken[seat] = SeatStatus.EMPTY
        else:
            taken[seat] = SeatStatus.FLOOR

    last = len([n for n in taken if n == SeatStatus.TAKEN])
    iteration = 0

    while True:
        current = copy.deepcopy(taken)
        # render_plane(current, width, iteration, taken_map)

        for seat in (i for i, loc in enumerate(flat) if loc == Location.SEAT):
            occupied = taken[seat] == SeatStatus.TAKEN
            others = check_seat(taken, width, seat)
            neighbors[seat] = others

            if occupied:
                if others < 4:
                    current[seat] = SeatStatus.TAKEN
                else:
                    current[seat] = SeatStatus.EMPTY
            else:
                if others == 0:
                    current[seat] = SeatStatus.TAKEN
                else:
                    current[seat] = SeatStatus.EMPTY

        # render_plane(neighbors, width, f"{iteration}-sum")
        seated = len([n for n in current if n == SeatStatus.TAKEN])

        if seated == last:
            print(f"\nAll Done, Seated: {last} (iteration: {iteration})")
            break
        else:
            sys.stdout.write(".")
            sys.stdout.flush()

        taken = current
        last = seated
        iteration += 1
