def parse_strs(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


def parse_scedule_exercise1(filepath):
    data = [l for l in parse_strs(filepath)]
    earliest = int(data[0])
    bus_ids = [int(id) for id in data[1].split(",") if id != "x"]

    return earliest, bus_ids


def parse_scedule_exercise2(filepath):
    data = [l for l in parse_strs(filepath)]
    bus_ids = [int(id) if id != "x" else id for id in data[1].split(",")]

    return bus_ids