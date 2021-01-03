from parser import parse_input

input = [l for l in parse_input("./data/full")]

output = list(map(lambda i: (i["code"], i["stored"]), input))
code, stored = [sum(i) for i in zip(*output)]

print(code, stored, code - stored)
