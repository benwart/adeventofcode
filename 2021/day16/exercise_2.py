#!/usr/bin/env python3

from collections import namedtuple
from functools import partial
from numpy import product
from operator import gt, lt, eq
from parser import parse_msg
from pprint import pprint

PacketHeader = namedtuple("PacketHeader", "V Tid")

def popleft(input, i) -> tuple[str, str]:
    return input[0:i], input[i:]


def bint(bin:str) -> int:
    return int(f"0b{bin}", base=2)


def parse_header(input: str, packet: "Packet"):
    # 3 bits packet version
    packet.V = bint(input[0:3])
    # 3 bits packet type
    packet.Tid = bint(input[3:6])

    return input[6:]


def parse_literal(input: str, packet: "Packet"):

    # literal value string in binary
    value_arr = list()

    # grab 5 bits
    length = len(input)
    for i in range(0, length, 5):
        if length >= i+5:

            # get the next 5 bits
            not_last, block = int(input[i]), input[i+1:i+5]

            # add to the value
            value_arr.append(block)

            # check if this is the last block
            if not not_last:
                break

    # assemble and convert to int
    packet.LITERAL = bint("".join(value_arr))

    return input[i+5:]


def parse_sub_packets_by_length(input: str, packet: "Packet") -> str:
    Lstr, r = popleft(input, 15) 
    length = bint(Lstr)
    packet.L = length
    subs, r = popleft(r, length)
    
    while len([s for s in subs if not s == 0]) > 0:
        p = Packet(subs)
        packet.PACKETS.append(p)
        subs = p.remaining

    return r


def parse_sub_packets_by_count(input: str, packet: "Packet") -> str:
    Lstr, r = popleft(input, 11)
    count = bint(Lstr)
    packet.L = count

    for _ in range(count):
        p = Packet(r)
        packet.PACKETS.append(p)
        r = p.remaining

    return r


ltypes = {
    0: parse_sub_packets_by_length,
    1: parse_sub_packets_by_count,
}


def parse_sub_packets(input: str, packet: "Packet"):
    # get mode of sub packet length
    packet.LTid, r = int(input[0]), input[1:]

    # call the right sub packet parser
    return ltypes[packet.LTid](r, packet)
    

parse_by_type = {
    0: parse_sub_packets,
    1: parse_sub_packets,
    2: parse_sub_packets,
    3: parse_sub_packets,
    4: parse_literal,
    5: parse_sub_packets,
    6: parse_sub_packets,
    7: parse_sub_packets,
}

packet_execute = partial(map, lambda p: p.execute())

execute_ops = {
    0: lambda p: sum(packet_execute(p.PACKETS)),
    1: lambda p: product(list(packet_execute(p.PACKETS))),
    2: lambda p: min(list(packet_execute(p.PACKETS))),
    3: lambda p: max(list(packet_execute(p.PACKETS))),
    4: lambda p: p.LITERAL,
    5: lambda p: 1 if gt(*list(packet_execute(p.PACKETS))) else 0,
    6: lambda p: 1 if lt(*list(packet_execute(p.PACKETS))) else 0,
    7: lambda p: 1 if eq(*list(packet_execute(p.PACKETS))) else 0,
}


class Packet(object):
    def __init__(self, input: str):
        # properties
        self.V: int = None
        self.Tid: int = None
        self.LITERAL: int = None
        self.LTid: int = None
        self.L: int = None
        self.PACKETS: list["Packet"] = []

        # parse packet
        r = parse_header(input, self)
        r = parse_by_type[self.Tid](r, self)
        
        # capture the leftover bits
        self.remaining = r

    def execute(self) -> int:
        return execute_ops[self.Tid](self)

    def version_sum(self) -> int:
        return self.V + sum(map(lambda p: p.version_sum(), self.PACKETS))

    def __str__(self) -> str:
        return pprint({ 
            "V": self.V, 
            "Tid": self.Tid, 
            "Value": self.execute(), 
            "Packets": list(map(str, self.PACKETS))
        }, indent=2)

    def __repr__(self) -> str:
        return f"Packet(V:{self.V},Tid:{self.Tid})"


if __name__ == "__main__":

    input = parse_msg("./2021/day16/data/full")

    print(f"Binary Input: {input}")

    packet = Packet(input)

    # pprint(str(packet))

    print(f"version sum: {packet.version_sum()}")
    print(f"execute: {packet.execute()}")
