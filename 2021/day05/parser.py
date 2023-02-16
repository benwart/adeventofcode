import re

line_regex = re.compile(r"(?P<x1>\d+),(?P<y1>\d+)\s+->\s+(?P<x2>\d+),(?P<y2>\d+)")


class Point(object):
    def __init__(self, x:str, y:str):
        self.x = int(x)
        self.y = int(y)

    def __str__(self):
        return f"{self.x},{self.y}"

    def __repr__(self):
        return f"Point({self})"


def parse_strs(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


def parse_vent_lines(filepath):
    for line in parse_strs(filepath):
        match = line_regex.match(line)
        if match:
            d = match.groupdict()
            vent = [Point(x=d["x1"], y=d["y1"]), Point(x=d["x2"], y=d["y2"])]
            yield vent


if __name__ == "__main__":
    list(parse_vent_lines("./2021/day05/data/example_1"))