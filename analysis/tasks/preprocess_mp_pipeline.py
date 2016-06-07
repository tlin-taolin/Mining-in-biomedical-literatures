# -*- coding: utf-8 -*-
#
# Clean the data of hp, and delete invalid file
#

import sys
sys.path.insert(0, 'parsing/mp/')


import parse_data


def main(path):
    parse_data.parsing(path)


if __name__ == '__main__':
    in_path = "data/mp"
    main(in_path)
