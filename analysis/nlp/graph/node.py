# -*- coding: utf-8 -*-
#
# Build a class for node

class Node(object):
    def __init__(self, line):
        super(Node, self).__init__()
        self.id = line[0]
        self.name = line[1]
        self.defi = line[2]
        self.is_a = line[3]
        self.synonym = line[4]
        self.alt_id = line[5]
