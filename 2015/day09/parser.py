import re

ROUTE_REGEX = re.compile(
    r"(?P<start>[^\s]+)\sto\s(?P<end>[^\s]+)\s=\s(?P<distance>\d+)"
)


def parse_lines(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


def parse_route(line):
    m = ROUTE_REGEX.match(line)
    if m:
        d = m.groupdict()
        d["distance"] = int(d["distance"])
        return d


def parse_input(filepath):
    for line in parse_lines(filepath):
        yield parse_route(line)