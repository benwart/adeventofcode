#!/usr/bin/env python3

import re

required_fields = ("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid")
field_names = required_fields + ("cid",)
fields_regex = f"(?P<key>{'|'.join(field_names)}):(?P<value>[^\\s]+)"


def split_fields(line):
    return re.findall(fields_regex, line)


def year_validator(field, value, minimum, maximum):
    valuei = int(value)
    four_chars = len(value) == 4
    greater_min = valuei >= minimum
    less_max = valuei <= maximum
    valid = four_chars and greater_min and less_max
    return valid


# byr (Birth Year) - four digits; at least 1920 and at most 2002.
def byr(value):
    return year_validator("byr", value, 1920, 2002)


# iyr (Issue Year) - four digits; at least 2010 and at most 2020.
def iyr(value):
    return year_validator("iyr", value, 2010, 2020)


# eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
def eyr(value):
    return year_validator("eyr", value, 2020, 2030)


# hgt (Height) - a number followed by either cm or in:
#                If cm, the number must be at least 150 and at most 193.
#                If in, the number must be at least 59 and at most 76.
hgt_check = {
    "cm": (150, 193),
    "in": (59, 76),
}


def hgt(value):
    match = re.match(r"(?P<height>\d+)(?P<units>cm|in)", value)
    if match:
        height = int(match.group("height"))
        units = match.group("units")
        check = hgt_check[units]
        return height >= check[0] and height <= check[1]

    return False


# hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
def hcl(value):
    match = re.match(r"#[0-9a-f]{6}", value)
    return match != None


# ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
def ecl(value):
    match = re.match(r"amb|blu|brn|gry|grn|hzl|oth", value)
    return match != None


# pid (Passport ID) - a nine-digit number, including leading zeroes.
def pid(value):
    match = re.match(r"^[0-9]{9}$", value)
    return match != None


# cid (Country ID) - ignored, missing or not.
def cid(value):
    return True


validators = {
    "byr": byr,
    "iyr": iyr,
    "eyr": eyr,
    "hgt": hgt,
    "hcl": hcl,
    "ecl": ecl,
    "pid": pid,
    "cid": cid,
}


def validate_record(record):
    required_keys_exist = all(key in record for key in required_fields)
    values_are_valid = all(validators[k](v) for k, v in record.items())
    return required_keys_exist and values_are_valid


def handle_record(record, valid):
    if validate_record(record):
        valid += 1
    return ({}, valid)


def update_partial_record(record):
    matches = split_fields(line)
    if matches:
        fields = {n[0]: n[1] for n in matches}
        record.update(fields)
    return record


valid = 0
with open("./data/full") as f:
    record = {}
    for line in f:
        if line == "\n":
            record, valid = handle_record(record, valid)
            continue

        record = update_partial_record(record)

    # catch the last one if there is any
    if len(record.keys()) > 0:
        record, valid = handle_record(record, valid)


print(f"Valid Records: {valid}")
