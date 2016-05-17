# -*- coding: utf-8 -*-
#
# Define a list of tool functions.
import re
import json
import shutil
from os import listdir, remove, path, makedirs


def is_file_exist(file_path, debug=False):
    is_exist = path.exists(file_path)
    if debug and is_exist:
        remove(file_path)
        return False
    return is_exist


def list_files(path):
    return [path + f for f in listdir(path)]


def delete_file(file_path):
    is_exist = path.exists(file_path)
    if is_exist:
        remove(file_path)


def read_from_json(in_path):
    with open(in_path, "rb") as f:
        return json.loads(f.read())


def get_file_size(in_path):
    try:
        size = path.getsize(in_path) / 1024.0
    except:
        size = 0
    return size


def filter_by_file_size(in_path):
    size = get_file_size(in_path)
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


def append_to_smallfile(data, o):
    files = list_files(o)
    len_of_o = len(files)
    if get_file_size(o + str(len_of_o - 1)) / 1024.0 < 30:
        out_path = o + "0" if len_of_o == 0 else o + str(len_of_o - 1)
    else:
        out_path = o + str(len_of_o)
    with open(out_path, "a") as f:
        out = ("\n".join(data) + "\n\n").encode('utf-8').lower()
        f.write(out)


def append_to_bigfile(path, data, o):
    doc_id = re.sub("\D+", "", path)
    with open(o, "a") as f:
        out = (doc_id + "::" + "...".join(data) + "\n").encode('utf-8').lower()
        f.write(out)
