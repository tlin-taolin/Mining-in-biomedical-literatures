# -*- coding: utf-8 -*-
#
#
# analyze the ngram relationship in the graph.
#
import sys
sys.path.insert(0, 'util/')


import groupby
import readwrite


def parse_line(line):
    splited = line.strip("\n").split("\t")
    return splited[0], splited[1], float(splited[2])


def parse_lines(in_path):
    lines = readwrite.read_from_txt(in_path)
    parsed_lines = [parse_line(line) for line in lines if line != "\n"]
    return parsed_lines


def group_by_term(parsed_lines, ind):
    grouped = groupby.group_by(parsed_lines, index=ind)
    return to_index_based(grouped)


def sort_by_distance(tmp):
    return sorted(tmp, key=lambda x: x[1])


def to_index_based(grouped):
    mydict = {}
    for key, value in grouped:
        tmp = [(v[1], v[2]) for v in value]
        mydict[key] = sort_by_distance(tmp)
    return mydict


def output_sorted_result(groupby_result, out_path):
    out_string = ""
    for key, value in groupby_result.items():
        out_string += "".join([key + "\t" + v[0] + "\t" + str(v[1]) + "\n" for v in value]) + "\n"
    readwrite.write_to_txt(out_string, out_path, type="w")


def output_topk_sorted_result(groupby_result, out_path, k):
    out_string = ""
    for key, value in groupby_result.items():
        out_string += "".join([key + "\t" + v[0] + "\t" + str(v[1]) + "\n" for v in value[: k]]) + "\n"
    readwrite.write_to_txt(out_string, out_path + "-top" + str(k), type="w")


def analysis(level):
    root_path = "/media/tlin/Data/dataset/experiment_result/" + level
    in_path = root_path + "processed/ngram"
    out_path = root_path + "processed/sorted_ngram"
    parsed_lines = parse_lines(in_path)
    groupby_result = group_by_term(parsed_lines, ind=0)
    output_sorted_result(groupby_result, out_path)
    output_topk_sorted_result(groupby_result, out_path, k=20)

if __name__ == '__main__':
    analysis()
