import re

INSTRUCTION_REGEX = re.compile(r"(?P<op>[a-zA-Z]+)\s+(?P<value>\d+)")


def parse_strs(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.rstrip()


def parse_instructions(filepath):
    for line in parse_strs(filepath):
         groupdict = INSTRUCTION_REGEX.match(line).groupdict()
         yield {
             "op": groupdict["op"],
             "value": int(groupdict["value"]),
         }
