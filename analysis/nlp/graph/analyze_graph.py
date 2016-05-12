# -*- coding: utf-8 -*-
#
# analyze the graph.

import logging
from math import fabs
from itertools import groupby


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', )


def analyze_snap_graph(graph, name_map, topk=10):
    logging.info("-----------------------------------------------------------")
    logging.info("number of graph: {n}" .format(n=graph.GetNodes()))
    degrees = [(n.GetId(), n.GetInDeg(), n.GetOutDeg()) for n in graph.Nodes()]
    sort_by_in_degrees = sorted(degrees, key=lambda x: -x[1])
    sort_by_out_degrees = sorted(degrees, key=lambda x: -x[2])

    logging.info("Top {r} In-degree: ".format(r=topk))
    top_in_nodes = sort_by_in_degrees[: topk]
    top_in_nodes_with_name = [(name_map[n[0]], n[1]) for n in top_in_nodes]
    # logging.info(top_in_nodes)
    logging.info(top_in_nodes_with_name)

    logging.info("Top {r} Out-degree: ".format(r=topk))
    top_out_nodes = sort_by_out_degrees[: topk]
    top_out_nodes_with_name = [(name_map[n[0]], n[2]) for n in top_out_nodes]
    # logging.info(top_out_nodes)
    logging.info(top_out_nodes_with_name)

    logging.info("Node with great in-degree and out-degree difference: ")
    degree_diff = [(id, fabs(in_d - out_d)) for (id, in_d, out_d) in degrees]
    sort_by_diff = sorted(degree_diff, key=lambda x: -x[1])
    top_diff_nodes = sort_by_diff[: topk]
    top_diff_nodes_with_name = [(name_map[n[0]], n[1]) for n in top_diff_nodes]
    # logging.info(top_diff_nodes)
    logging.info(top_diff_nodes_with_name)


def analyze_igraph_graph(graph, topk=10):
    logging.info("-----------------------------------------------------------")
    sorted_edge = sorted(graph.get_edgelist(), key=lambda x: x[0])
    extract_edge = lambda x: x[1]
    grouped_edge = dict((k, map(extract_edge, list(e))) for k, e in groupby(sorted_edge, lambda x: x[0]))
    if_cyclic = is_cyclic_directed(grouped_edge)
    logging.info("Check if the graph is cyclic: {r}".format(r=if_cyclic))


def is_cyclic_directed(g):
    """Return True if the directed graph g has a cycle.
    g must be represented as a dictionary mapping vertices to
    iterables of neighbouring vertices. For example:

    >>> cyclic({1: (2,), 2: (3,), 3: (1,)})
    True
    >>> cyclic({1: (2,), 2: (3,), 3: (4,)})
    False
    """
    path = set()
    visited = set()

    def visit(vertex):
        if vertex in visited:
            return False
        visited.add(vertex)
        path.add(vertex)
        for neighbour in g.get(vertex, ()):
            if neighbour in path or visit(neighbour):
                return True
        path.remove(vertex)
        return False
    return any(visit(v) for v in g)


def convert_to_undirected(g):
    ng = {}
    for node, nodes in g.items():
        tmp = ng.get(node, ())
        ng[node] = tmp + nodes
        for n in nodes:
            tmp = ng.get(n, ())
            ng[n] = tmp + (node, )
    return dict([(key, tuple(set(value))) for key, value in ng.items()])


def is_cyclic_undirected(g, isdirected=False):
    """Return True if the undirected graph g has a cycle.
    g must be represented as a dictionary mapping vertices to
    iterables of neighbouring vertices

    It currently has a typo that if a <-> b, it will be regarded as a cycle.
    Indeed, it is not.
    """
    if is_cyclic_directed:
        g = convert_to_undirected(g)
    # directly use the alogrithm `is_cyclic_directed`
    return is_cyclic_directed(g)
