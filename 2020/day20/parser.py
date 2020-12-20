import re


str_to_value = {
    ".": "0",
    "#": "1",
}


class Edge:
    def __init__(self, tile_id, edge):
        self.tile_id = tile_id
        self.edge = edge
        self.value = "".join([str_to_value[n] for n in edge])
        self.rvalue = "".join([str_to_value[n] for n in reversed(edge)])

    def __repr__(self):
        return self.edge

    def __hash__(self):
        return min(int(self.value), int(self.rvalue))

    def __eq__(self, other):
        return hash(self) == hash(other)


def get_edges(tile_id, image):
    edges = [
        Edge(tile_id, image[0]),  # top
        Edge(tile_id, image[-1]),  # bottom
        Edge(tile_id, "".join([row[0] for row in image])),  # left
        Edge(tile_id, "".join([row[-1] for row in image])),  # right
    ]
    return set(edges)


class Tile:
    def __init__(self, tile_id, image):
        self.tile_id = int(tile_id)
        self.image = image
        self.edges = get_edges(self.tile_id, self.image)
        assert len(self.edges) == 4

    def matched_edges(self, other):
        return len(self.edges.intersection(other.edges))

    def __repr__(self):
        return f"Tile: {self.tile_id}"


TILE_NAME_REGEX = re.compile(r"^Tile\s(?P<id>\d+):$")


def parse_tile(lines):
    id = TILE_NAME_REGEX.match(lines[0]).groupdict()["id"]
    image = lines[1:]
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