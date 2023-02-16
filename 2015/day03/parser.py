from collections import namedtuple

Direction = namedtuple("Position", ("x", "y"))

translation = {
    "^": Direction(x=0, y=1),
    ">": Direction(x=1, y=0),
    "<": Direction(x=-1, y=0),
    "v": Direction(x=0, y=-1),
}


def chunks(filename, buffer_size=1):
    with open(filename, "rb") as fp:
        chunk = fp.read(buffer_size)
        while chunk:
            yield chunk
            chunk = fp.read(buffer_size)


def parse_directions(filename, buffersize=1):
    for chunk in chunks(filename, buffersize):
        for char in chunk:
            yield translation[chr(char)]
