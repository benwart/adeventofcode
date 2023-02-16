#!/usr/bin/env python3

"""
--- Part Two ---
As you finish the last group's customs declaration, you notice that you misread one word in the instructions:

You don't need to identify the questions to which anyone answered "yes"; you need to identify the questions to which everyone answered "yes"!

Using the same example as above:

abc

a
b
c

ab
ac

a
a
a
a

b

This list represents answers from five groups:

In the first group, everyone (all 1 person) answered "yes" to 3 questions: a, b, and c.
In the second group, there is no question to which everyone answered "yes".
In the third group, everyone answered yes to only 1 question, a. Since some people did not answer "yes" to b or c, they don't count.
In the fourth group, everyone answered yes to only 1 question, a.
In the fifth group, everyone (all 1 person) answered "yes" to 1 question, b.
In this example, the sum of these counts is 3 + 0 + 1 + 1 + 1 = 6.

For each group, count the number of questions to which everyone answered "yes". What is the sum of those counts?
"""

# Not needing as set.intersection(*sets) does all this (likely faster)
#
# def get_answers(anaswers):
#     size = len(answers)
#     counts = {chr(i): 0 for i in range(97, 123)}
#     for a in answers:
#         for c in a:
#             counts[c] += 1

#     # print([c for c, l in counts.items() if l > 0])
#     output = "".join([c for c, l in counts.items() if l == size])
#     # print(output)
#     return output

groups = []

with open("./data/full") as f:
    answers = []
    for line in f:
        if line == "\n":
            groups.append(set.intersection(*answers))
            answers = []
            continue

        answers.append(set([c for c in line.rstrip()]))

    if len(answers) > 0:
        groups.append(set.intersection(*answers))

# print(groups)
print(f"Sum of counts: {sum(map(lambda x: len(x), groups))}")
