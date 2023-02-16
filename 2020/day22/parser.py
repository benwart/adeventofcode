import re
from collections import deque


def parse_lines(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


def parse_player(lines):
    id = int(re.match(r"Player\s+(?P<id>\d+):", lines[0]).groupdict()["id"])
    cards = deque()
    for line in lines[1:]:
        cards.appendleft(int(line))
    return {"id": id, "cards": cards}


def parse_input(filepath):
    lines = []
    players = []
    for line in parse_lines(filepath):
        if len(line) == 0:
            players.append(parse_player(lines))
            lines = []
        else:
            lines.append(line)
    players.append(parse_player(lines))
    return players