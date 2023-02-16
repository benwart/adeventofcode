#!/usr/bin/env python3

from parser import parse_instruction


move_cardinal = {
    "E": (1, 0),
    "N": (0, 1),
    "W": (-1, 0),
    "S": (0, -1),
}

move_forward = {
    0: (1, 0),
    90: (0, 1),
    180: (-1, 0),
    270: (0, -1),
}


class Ferry:
    def __init__(self):
        self.heading = 0
        self.x = 0
        self.y = 0

    def manhatten_distance(self):
        return abs(self.x) + abs(self.y)

    def rotate(self, direction, degrees):
        self.heading += degrees if direction == "L" else 360 - (degrees % 360)
        self.heading = self.heading % 360

    def move(self, transform, value):
        self.x += transform[0] * value
        self.y += transform[1] * value

    def move_forward(self, value):
        transform = move_forward[self.heading]
        self.move(transform, value)

    def move_cardinal(self, cardinal, value):
        transform = move_cardinal[cardinal]
        self.move(transform, value)

    def execute_instruction(self, instruction):
        op = instruction["op"]
        value = instruction["value"]

        if op in ["N", "S", "E", "W"]:
            self.move_cardinal(op, value)
        elif op in ["L", "R"]:
            self.rotate(op, value)
        else:
            self.move_forward(value)


ferry = Ferry()

for instruction in parse_instruction("./data/full"):
    ferry.execute_instruction(instruction)

print(f"Manhatten Distance from Start: {ferry.manhatten_distance()}")