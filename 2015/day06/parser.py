import re

# turn on 0,0 through 999,999
# toggle 0,0 through 999,0
# turn off 499,499 through 500,500
COMMAND_REGEX = re.compile(
    r"^(?P<command>[^\d]+)\s(?P<x1>\d+),(?P<y1>\d+)\sthrough\s(?P<x2>\d+),(?P<y2>\d+)$"
)


class Command:
    def __init__(self, command, x1, y1, x2, y2):
        self.command = command
        self.x1 = int(x1)
        self.y1 = int(y1)
        self.x2 = int(x2)
        self.y2 = int(y2)

    def __repr__(self):
        return f"{self.command}: {self.x1},{self.y1} - {self.x2},{self.y2}"

    def range(self):
        return (
            self.x1,
            self.y1,
            self.x2,
            self.y2,
        )


def parse_strs(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


def parse_commands(filepath):
    for line in parse_strs(filepath):
        match = COMMAND_REGEX.match(line).groupdict()
        yield Command(**match)
