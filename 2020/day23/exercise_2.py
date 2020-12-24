#!/usr/bin/env python3

import progressbar
from collections import namedtuple
from linkedlist import DoubleLinkedList, ListNode
from math import prod

Input = namedtuple("Input", "value, answer")

example1 = Input("389125467", "67384529")
full = Input("974618352", None)


def iter_links(head):
    n = head
    while n != None:
        yield n.value
        n = n.next


def simulate(input, max_value=1000000, stop=10000000, bar=None):
    stop += 1
    max_value += 1

    cups = list(map(int, input))
    cups.extend([i for i in range(max(cups) + 1, max_value)])

    # convert to linkedlist
    linked = DoubleLinkedList()
    n = ListNode(linked, cups[0])
    for cup in cups[1:]:
        n = n.push(cup)

    curr = linked.find(cups[0])

    # make circular link
    curr.prev, n.next = n, curr

    for move in range(1, stop):

        # pickup 3 cups
        pickup = curr.remove(3)

        # select next cup
        dest = None
        look = curr.value

        while dest == None:
            look = (max_value + look - 1) % max_value
            if look not in pickup and look != 0:
                dest = linked.find(look)

        # insert picked up cups
        dest.insert(pickup.head, pickup.tail)

        # update curr
        curr = curr.next

        if bar:
            bar.update(move)

    # shift cups to get answer
    output = linked.find(1).remove(2)
    # return f"{''.join(map(str, iter_links(output.head)))}"

    return prod(iter_links(output.head))

    # print(prod(cups[i % len(cups)] for i in range(start + 1, start + 3)))


if __name__ == "__main__":
    max_value = 1000000
    stop = 10000000
    with progressbar.ProgressBar(max_value=stop) as bar:
        results = simulate(example1.value, max_value=max_value, stop=stop, bar=bar)

    print(results)