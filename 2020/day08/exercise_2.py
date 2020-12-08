#!/usr/bin/env python3

"""
--- Part Two ---
After some careful analysis, you believe that exactly one instruction is corrupted.

Somewhere in the program, either a jmp is supposed to be a nop, or a nop is supposed to be a jmp. (No acc instructions were harmed in the corruption of this boot code.)

The program is supposed to terminate by attempting to execute an instruction immediately after the last instruction in the file. By changing exactly one jmp or nop, you can repair the boot code and make it terminate correctly.

For example, consider the same program from above:

nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6

If you change the first instruction from nop +0 to jmp +0, it would create a single-instruction infinite loop, never leaving that instruction. If you change almost any of the jmp instructions, the program will still eventually find another jmp instruction and loop forever.

However, if you change the second-to-last instruction (from jmp -4 to nop -4), the program terminates! The instructions are visited in this order:

nop +0  | 1
acc +1  | 2
jmp +4  | 3
acc +3  |
jmp -3  |
acc -99 |
acc +1  | 4
nop -4  | 5
acc +6  | 6

After the last instruction (acc +6), the program terminates by attempting to run the instruction below the last instruction in the file. With this change, after the program terminates, the accumulator contains the value 8 (acc +1, acc +1, acc +6).

Fix the program so that it terminates normally by changing exactly one jmp (to nop) or nop (to jmp). What is the value of the accumulator after the program terminates?
"""

from parser import instructions


def switch(op):
    if op == "jmp":
        return "nop"
    if op == "nop":
        return "jmp"
    return op


def nop(n, i, a):
    i += 1
    return i, a


def acc(n, i, a):
    a += n
    i += 1
    return i, a


def jmp(n, i, a):
    i += n
    return i, a


operations = {
    "nop": nop,
    "acc": acc,
    "jmp": jmp,
}


def run(program, swap=None):
    index = 0
    accumulator = 0
    visited = set()

    while True:
        # get instruction from program
        instruction = program[index]

        if index == swap:
            instruction["op"] = switch(instruction["op"])
            # print(f"{index}: {instruction} (swap)")

        # print(f"{index} ({accumulator}): {instruction}")

        if index in visited:
            return (False, f"Found Cycle. ACC: {accumulator}", visited)

        visited.add(index)

        # handle instruction
        index, accumulator = operations[instruction["op"]](
            instruction["value"], index, accumulator
        )

        if len(program) <= index:
            return (
                True,
                f"Success we are done with the program: {accumulator}",
                visited,
            )


# -------------------------------------------------------

original = [i for i in instructions("./data/full")]
done, message, failed_visited = run(original)

sorted_visited = sorted(failed_visited)


for v in sorted_visited:
    o = original[v]
    if o["op"] in ["jmp", "nop"]:
        # print(f"{v}: {o['op']} => {switch(o['op'])}")
        done, message, visited = run([i for i in instructions("./data/full")], v)
        if done:
            print(message)
            break
