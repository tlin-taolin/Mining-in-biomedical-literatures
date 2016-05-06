# -*- coding: utf-8 -*-
#
# Define a list of tool functions.
import json
from os import listdir, remove, path, makedirs
import shutil

def is_file_exist(file_path, debug=False):
    is_exist = path.exists(file_path)
    if debug and is_exist:
        remove(file_path)
        return False
    return is_exist


def list_files(in_path):
    path = in_path + "parsed/"
    return [in_path + "parsed/" + f for f in listdir(path)]


def delete_file(file_path):
    is_exist = path.exists(file_path)
    if is_exist:
        remove(file_path)


def read_from_json(in_path):
    with open(in_path, "rb") as f:
        return json.loads(f.read())


def check_file_size(in_path):
    size = path.getsize(in_path) / 1024.0
    if size > 10:
        sdata = read_from_json(in_path)
        return sdata, True
    else:
        return None, False


def mkdir(root_path, p):
    file_path = root_path + p
    is_exist = path.exists(file_path)
    if is_exist:
        shutil.rmtree(file_path, ignore_errors=True)
    makedirs(file_path)


def write_to_json(data, out_path):
    with open(out_path, "w") as f:
        json.dump(data, f)
