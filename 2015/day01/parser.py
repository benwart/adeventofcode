#!/usr/bin/env python3


def chunks(filename, buffer_size=4096):
    with open(filename, "rb") as fp:
        chunk = fp.read(buffer_size)
        while chunk:
            yield chunk
            chunk = fp.read(buffer_size)


def chars(filename, buffersize=4096):
    for chunk in chunks(filename, buffersize):
        for char in chunk:
            yield chr(char)
