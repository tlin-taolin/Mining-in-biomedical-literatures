# -*- coding: utf-8 -*-
#
# Define a list of tool functions for check file operation
#

import shutil
from readwrite import *
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


def mkdir(file_path):
    is_exist = path.exists(file_path)
    if is_exist:
        shutil.rmtree(file_path, ignore_errors=True)
    makedirs(file_path)


def get_file_size(in_path):
    try:
        size = path.getsize(in_path) / 1024.0
    except:
        size = 0
    return size


def filter_by_file_size(in_path, in_size):
    size = get_file_size(in_path)
    if size > in_size:
        sdata = read_from_json(in_path)
        return sdata, True
    else:
        return None, False
