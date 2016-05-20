# -*- coding: utf-8 -*-
#
# analyze the graph.

import sys
sys.path.insert(0, 'util/')
import is_directed_graph_cyclic

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
    if_cyclic = is_directed_graph_cyclic.is_cyclic_directed(grouped_edge)
    logging.info("Check if the graph is cyclic: {r}".format(r=if_cyclic))
