# -*- coding: utf-8 -*-
#
# Clean the data of hp, and delete invalid file
#

import sys
sys.path.insert(0, 'parsing/hp/')

import clean_data
import statistics


def main(path):
    clean_data.parsing_and_clean()
    statistics.stat(path)

if __name__ == '__main__':
    in_name_path = "data/hp/parsed_name"
    main(in_name_path)
