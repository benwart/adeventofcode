#!/usr/bin/env python3

from parser import parse_instruction


move_cardinal = {
    "E": (1, 0),
    "N": (0, 1),
    "W": (-1, 0),
    "S": (0, -1),
}


class Ferry:
    def __init__(self, f_x=0, f_y=0, w_x=10, w_y=1):
        self.origin_x = f_x
        self.origin_y = f_y
        self.f_x = f_x
        self.f_y = f_y
        self.w_x = w_x
        self.w_y = w_y

    def manhatten_distance(self):
        return abs(self.origin_x - self.f_x) + abs(self.origin_y - self.f_y)

    def rotate(self, direction, degrees):
        heading = degrees % 360 if direction == "L" else 360 - (degrees % 360)

        x = self.w_x
        y = self.w_y

        if heading == 90:
            self.w_x = -y
            self.w_y = x

        elif heading == 180:
            self.w_x *= -1
            self.w_y *= -1

        elif heading == 270:
            self.w_x = y
            self.w_y = -x

    def move_forward(self, value):
        self.f_x += self.w_x * value
        self.f_y += self.w_y * value

    def move_cardinal(self, cardinal, value):
        transform = move_cardinal[cardinal]
        self.w_x += transform[0] * value
        self.w_y += transform[1] * value

    def execute_instruction(self, instruction):
        op = instruction["op"]
        value = instruction["value"]

        if op in ["N", "S", "E", "W"]:
            self.move_cardinal(op, value)
        elif op in ["L", "R"]:
            self.rotate(op, value)
        else:
            self.move_forward(value)


ferry = Ferry(0, 0, 10, 1)

for instruction in parse_instruction("./data/full"):
    ferry.execute_instruction(instruction)

print(f"Manhatten Distance from Start: {ferry.manhatten_distance()}")