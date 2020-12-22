#!/usr/bin/env python3

import sqlite3
from parser import parse_foods


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def setup_schema(db):
    with open("./schema.sql") as f:
        schema = f.read()

    c = db.cursor()
    c.executescript(schema)
    db.commit


def insert_allergens(db, food):

    builder = ["INSERT INTO allergens (food_id, name) VALUES "]
    builder.append(
        ", ".join([f"({food['id']}, '{name}')" for name in food["allergens"]])
    )
    builder.append(";")
    statement = "".join(builder)

    c = db.cursor()
    c.execute(statement)


def insert_ingredients(db, food):

    builder = ["INSERT INTO ingredients (food_id, name) VALUES "]
    builder.append(
        ", ".join([f"({food['id']}, '{name}')" for name in food["ingredients"]])
    )
    builder.append(";")
    statement = "".join(builder)

    c = db.cursor()
    c.execute(statement)


def insert_food(db, food):
    c = db.cursor()
    c.execute("INSERT INTO foods (id) VALUES (:id);", {"id": food["id"]})
    insert_ingredients(db, food)
    insert_allergens(db, food)


def get_allergens(db):
    c = db.cursor()

    output = []
    for r in c.execute("SELECT DISTINCT name FROM allergens;"):
        output.append(r)

    return output


def foods_with_allergen(db, allergen):
    c = db.cursor()
    c.execute(
        """
    SELECT COUNT(f.id) AS food
      FROM foods AS f
        LEFT JOIN allergens AS a ON f.id = a.food_id 
     WHERE a.name = ':allergen';
    """,
        {"allergen": allergen},
    )
    return c.fetchone()


with sqlite3.connect("./data/exercise_1.db") as db:
    db.row_factory = dict_factory
    setup_schema(db)

    # setup

    for food in parse_foods("./data/example1"):
        insert_food(db, food)

    db.commit()

    # find list of ingredients that are common to all foods with given allergen

    allergens = get_allergens(db)
    for allergen in allergens:
        print(
            f"Count of Food with {allergen['name']}: {foods_with_allergen(db, allergen['name'])}"
        )
