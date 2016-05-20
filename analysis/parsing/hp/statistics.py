# -*- coding: utf-8 -*-
#
# Do the statistics for the parsed results.

import sys
sys.path.insert(0, 'util/')
import readwrite

import numpy as np
import matplotlib.pyplot as plt


def split_name(names):
    return [name.strip("\n").split(" ") for name in names]


def get_len_name(splitted_name):
    return map(len, splitted_name)


def min_len(len_of_name):
    return min(len_of_name)


def max_len(len_of_name):
    return max(len_of_name)


def median_len(len_of_name):
    return np.median(len_of_name)


def plot_hist_len(len_of_name):
    plt.hist(len_of_name)
    plt.title("Histogram of the name length")
    plt.xlabel("Length of name")
    plt.ylabel("Frequency")
    plt.savefig('hist_of_len_name.pdf')


def stat(inpath):
    names = readwrite.read_from_txt(inpath)
    splitted_name = split_name(names)
    len_name = get_len_name(splitted_name)
    plot_hist_len(len_name)
    print "The minimal of name length: {r}" .format(r=min_len(len_name))
    print "The maximal of name length: {r}" .format(r=max_len(len_name))
    print "The median of name length: {r} " .format(r=median_len(len_name))


if __name__ == '__main__':
    in_name_path = "data/graph/parsed_name"
    stat(in_name_path)
