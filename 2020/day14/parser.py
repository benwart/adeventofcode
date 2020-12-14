import re


def parse_strs(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


def parse_mask(line):
    """ mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X """
    return line.split(" = ")[1].strip()


def parse_mem(line, mask):
    """ mem[8] = 11 """
    match = re.match(r"^mem\[(?P<address>\d+)\]\s=\s(?P<value>\d+)$", line).groupdict()
    output = {}
    output["address"] = int(match["address"])
    output["value"] = int(match["value"])
    output["mask"] = mask
    return output


def parse_program(filepath):
    mask = None
    for line in parse_strs(filepath):
        if line.startswith("mask"):
            mask = parse_mask(line)
        elif line.startswith("mem"):
            yield parse_mem(line, mask)
