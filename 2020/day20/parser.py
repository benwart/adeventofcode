import re


from tile import Tile

str_to_value = {
    ".": 0,
    "#": 1,
}
TILE_NAME_REGEX = re.compile(r"^Tile\s(?P<id>\d+):$")


def parse_tile(lines):
    id = TILE_NAME_REGEX.match(lines[0]).groupdict()["id"]
    image = [[str_to_value[c] for c in line] for line in lines[1:]]
    return Tile(id, image)


def parse_lines(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


def parse_input(filepath):
    lines = []
    for line in parse_lines(filepath):
        if len(line) == 0:
            yield parse_tile(lines)
            lines = []
        else:
            lines.append(line)

    if len(lines):
        yield parse_tile(lines)