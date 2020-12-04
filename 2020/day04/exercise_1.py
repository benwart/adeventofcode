#!/usr/bin/env python3

import re

# byr (Birth Year)
# iyr (Issue Year)
# eyr (Expiration Year)
# hgt (Height)
# hcl (Hair Color)
# ecl (Eye Color)
# pid (Passport ID)
# cid (Country ID)

required_fields = ("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid")
field_names = required_fields + ("cid",)
fields_regex = f"(?P<key>{'|'.join(field_names)}):(?P<value>[^\\s]+)"


def split_fields(line):
    return re.findall(fields_regex, line)


def validate_record(record):
    return all(key in record for key in required_fields)


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
