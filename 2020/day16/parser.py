import re

FIELD_REGEX = re.compile(
    r"(?P<name>[^:]+):\s(?P<min1>\d+)-(?P<max1>\d+)\sor\s(?P<min2>\d+)-(?P<max2>\d+)"
)


def parse_fields(f):
    fields = {}

    while True:
        line = f.readline().rstrip()
        if line == "":
            return fields

        m = FIELD_REGEX.match(line)
        if m:
            d = m.groupdict()
            fields[d["name"]] = [
                (int(d["min1"]), int(d["max1"])),
                (int(d["min2"]), int(d["max2"])),
            ]


def parse_ticket(line):
    return [i for i in map(lambda num: int(num), line.split(","))]


def parse_your_ticket(f):
    while True:
        line = f.readline().rstrip()
        if line == "your ticket:":
            return parse_ticket(f.readline().rstrip())


def parse_nearby_tickets(f):
    tickets = []
    for line in f:
        stripped = line.rstrip()
        if stripped in ("nearby tickets:", ""):
            continue

        tickets.append(parse_ticket(stripped))
    return tickets


def parse_data(filepath):
    with open(filepath) as f:
        return {
            "fields": parse_fields(f),
            "ticket": parse_your_ticket(f),
            "nearby": parse_nearby_tickets(f),
        }
