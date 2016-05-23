# -*- coding: utf-8 -*-
#
#

from itertools import groupby


def group_by(data, index):
    sorted_data = sorted(data, key=lambda x: x[index])
    groupby_data = groupby(sorted_data, lambda x: x[index])
    return groupby_data
    
