# -*- coding: utf-8 -*-
#
#
# A script to process the ngram data
#

import re
import sys
sys.path.insert(0, 'util/')
import opfiles
import readwrite


def get_all_files(root_path):
    sub_path = root_path + "origin/ngram-result/"
    ngrams = list("1")
    folders = [sub_path + "statScore-{s}/".format(s=ng) for ng in ngrams]
    files = [opfiles.list_files(p) for p in folders]
    return files


def parse_line(line, regex):
    return re.findall(regex, line)[0]


def parse_lines(root_path, out_path):
    opfiles.is_file_exist(out_path, debug=True)
    pattern = r"\(\((.*?),(.*?)\),(.*?)\)"
    regex = re.compile(pattern, re.S)
    files_paths = get_all_files(root_path)

    for files in files_paths:
        for file in files:
            data = readwrite.read_from_txt(file)
            parsed = [parse_line(d, regex) for d in data]
            out_string = "\n".join(["\t".join(p) for p in parsed]) + "\n"
            readwrite.write_to_txt(out_string, out_path, type="a")


def cleaning(level):
    root_path = "/media/tlin/Data/dataset/experiment_result/" + level
    out_path = root_path + "processed/ngram"
    parse_lines(root_path, out_path)


if __name__ == '__main__':
    cleaning()
