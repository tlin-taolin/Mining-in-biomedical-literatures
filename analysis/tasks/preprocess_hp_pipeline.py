# -*- coding: utf-8 -*-
#
# Clean the data of hp, and delete invalid file
#

import sys
sys.path.insert(0, 'parsing/hp/')

import clean_data
import statistics


if __name__ == '__main__':
    clean_data.parsing_and_clean()
    in_name_path = "data/graph/parsed_name"
    statistics.stat(in_name_path)
