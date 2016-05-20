# -*- coding: utf-8 -*-
#
#
# A script to process the ngram data
#

import re
from os import listdir, remove, path


def is_file_exist(file_path, debug=False):
    is_exist = path.exists(file_path)
    if debug and is_exist:
        remove(file_path)
        return False
    return is_exist


def list_files(path):
    return [path + f for f in listdir(path)]


def read_data(path):
    with open(path, "r") as f:
        return f.readlines()


def get_all_files(root_path):
    sub_path = root_path + "origin/ngram-result/"
    ngrams = list("1")
    folders = [sub_path + "statScore-{s}/".format(s=ng) for ng in ngrams]
    files = [list_files(p) for p in folders]
    return files


def parse_line(line, regex):
    return re.findall(regex, line)[0]


def parse_lines(root_path, out_path):
    is_file_exist(out_path, debug=True)
    pattern = r"\(\((.*?),(.*?)\),(.*?)\)"
    regex = re.compile(pattern, re.S)
    files_paths = get_all_files(root_path)

    for files in files_paths:
        for file in files:
            data = read_data(file)
            parsed = [parse_line(d, regex) for d in data]
            tmp = "\n".join(["\t".join(p) for p in parsed])
            with open(out_path, "a") as w:
                w.write(tmp.encode("utf-8"))


def main():
    root_path = "/media/tlin/Data/dataset/experiment_result/"
    out_path = root_path + "processed/ngram"
    parse_lines(root_path, out_path)


if __name__ == '__main__':
    main()
