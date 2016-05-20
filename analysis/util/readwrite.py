# -*- coding: utf-8 -*-
#
# Define a list of tool functions for read and write.
#

import json


def read_from_json(in_path):
    with open(in_path, "rb") as f:
        return json.loads(f.read())


def write_to_json(data, out_path):
    with open(out_path, "w") as f:
        json.dump(data, f)


def read_from_txt(in_path):
    with open(in_path, "rb") as f:
        return f.readlines()


def write_to_txt(data, out_path, type="w"):
    with open(out_path, type) as f:
        f.write(data.encode("utf-8"))
