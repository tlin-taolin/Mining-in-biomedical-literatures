# -*- coding: utf-8 -*-
#
#

def convert_to_undirected(g):
    ng = {}
    for node, nodes in g.items():
        tmp = ng.get(node, ())
        ng[node] = tmp + nodes
        for n in nodes:
            tmp = ng.get(n, ())
            ng[n] = tmp + (node, )
    return dict([(key, tuple(set(value))) for key, value in ng.items()])
