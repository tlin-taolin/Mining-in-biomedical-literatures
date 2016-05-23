# -*- coding: utf-8 -*-
#
# Generate a 'random' graph based on given relationship matrix
# and pre-defined rule.

import copy
import logging
from random import seed, sample
import extract_relationship_phenotype
import is_directed_graph_cyclic


def graph_generation_naive(pairwise_distance, top=30, inseed=6666666):
    seed(inseed)
    knn_dict, group_list = extract_relationship_phenotype.select_topk(pairwise_distance, topk=top)

    nodes = knn_dict.keys()
    nodes_edges = dict([(key, map(lambda x: x[0], value)) for key, value in knn_dict.items()])
    origin_graph = dict([(value[0], map(lambda x: x[0], value[1])) for value in group_list])

    random_pick_node = lambda x: sample(nodes, 1)[0]
    random_pick_node_neighbor = lambda x: sample(nodes_edges[x], 1)[0]

    graph = {}

    logging.info("Create a acyclic directed graph.")
    while True:
        start_node = random_pick_node(nodes)
        start_node_edge = random_pick_node_neighbor(start_node)
        edges = graph.get(start_node, ())
        if start_node_edge in edges:
            continue
        new_graph = copy.deepcopy(graph)
        new_graph[start_node] = new_graph.get(start_node, ()) + (start_node_edge, )
        if is_directed_graph_cyclic.is_cyclic_directed(new_graph):
            cur_num_nodes = len(new_graph.keys())
            if cur_num_nodes > 3.0 / 4 * len(nodes):
                return origin_graph, new_graph
            else:
                logging.info("Does not reach the threshold, current node number: {r}" .format(r=cur_num_nodes))
        else:
            graph = new_graph


def graph_generation_normal(pairwise_distance, top=30, inseed=6666666):
    pass
