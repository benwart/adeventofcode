from parser import parse_input

input = [l for l in parse_input("./data/full")]

output = list(map(lambda i: (i["code"], i["stored"], i["encoded"]), input))
code, stored, encoded = [sum(i) for i in zip(*output)]

print(code, stored, encoded, encoded - code)
