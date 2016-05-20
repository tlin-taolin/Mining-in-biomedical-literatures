# -*- coding: utf-8 -*-
#
#

import sys
sys.path.insert(0, 'util/')
import is_directed_graph_cyclic
import directedG_to_undirectedG

def is_cyclic_undirected(g, isdirected=False):
    """Return True if the undirected graph g has a cycle.
    g must be represented as a dictionary mapping vertices to
    iterables of neighbouring vertices

    It currently has a typo that if a <-> b, it will be regarded as a cycle.
    Indeed, it is not.
    """
    if is_directed_graph_cyclic.is_cyclic_directed:
        g = directedG_to_undirectedG.convert_to_undirected(g)
    # directly use the alogrithm `is_cyclic_directed`
    return is_directed_graph_cyclic.is_cyclic_directed(g)
