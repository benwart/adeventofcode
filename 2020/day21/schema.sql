--
-- File generated with SQLiteStudio v3.1.1 on Sun Dec 20 21:39:58 2020
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = OFF;

BEGIN TRANSACTION;

-- Table: allergens
DROP TABLE IF EXISTS allergens;

CREATE TABLE allergens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    food_id INTEGER REFERENCES foods (id) NOT NULL,
    name TEXT NOT NULL
);

-- Table: foods
DROP TABLE IF EXISTS foods;

CREATE TABLE foods (id INTEGER PRIMARY KEY);

-- Table: ingredients
DROP TABLE IF EXISTS ingredients;

CREATE TABLE ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    food_id INTEGER REFERENCES foods (id) NOT NULL,
    name TEXT NOT NULL
);

COMMIT TRANSACTION;

PRAGMA foreign_keys = ON;