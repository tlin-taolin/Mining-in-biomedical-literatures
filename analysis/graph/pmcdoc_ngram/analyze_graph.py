# -*- coding: utf-8 -*-
#
#
# analyze the ngram relationship in the graph.
#
import sys
sys.path.insert(0, 'util/')

import readwrite


def parse_line(line):
    splited = line.strip("\n").split("\t")
    return splited[0], splited[1], float(splited[2])


def parse_lines(in_path):
    lines = readwrite.read_from_txt(in_path)
    parsed_lines = [parse_line(line) for line in lines if line != "\n"]


def _analysis():
    root_path = "/media/tlin/Data/dataset/experiment_result/"
    in_path = root_path + "processed/ngram"
    parse_lines(in_path)


if __name__ == '__main__':
    _analysis()
