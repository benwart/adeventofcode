#!/usr/bin/env python3

from collections import defaultdict
from parser import parse_foods

allergens = {}
occurrences = defaultdict(lambda: 0)

for food in parse_foods("./data/full"):

    for allergen in food["allergens"]:
        if allergen in allergens:
            allergens[allergen] = [
                i for i in food["ingredients"] if i in allergens[allergen]
            ]
        else:
            allergens[allergen] = [i for i in food["ingredients"]]

    for ingredient in food["ingredients"]:
        occurrences[ingredient] += 1

count = 0
for ingredient, times in occurrences.items():
    if all(ingredient not in v for v in allergens.values()):
        count += times

used = set()
while any(len(a) > 1 for a in allergens.values()):
    for allergen, ingredient in allergens.items():
        if len(ingredient) == 1 and ingredient[0] not in used:
            used.add(ingredient[0])
        elif len(ingredient) > 1:
            for i in used:
                if i in ingredient:
                    allergens[allergen].remove(i)

ingredients = ",".join(v[0] for k, v in sorted(allergens.items(), key=lambda k: k[0]))

print(ingredients)