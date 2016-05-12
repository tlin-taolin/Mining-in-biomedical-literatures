# -*- coding: utf-8 -*-
#
# Generate a 'random' graph based on given relationship matrix
# and pre-defined rule.

import copy
import logging
import numpy as np
from analyze_graph import *
from random import seed, sample
from itertools import combinations
from joblib import Parallel, delayed
from extract_relationship_phenotype import *


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', )


def generate_random_graph(pairwise_distance, top=30, inseed=6666666):
    seed(inseed)
    knn_dict, group_list = select_topk(pairwise_distance, topk=top)

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
        if is_cyclic_directed(new_graph):
            cur_num_nodes = len(new_graph.keys())
            if cur_num_nodes > 3.0 / 4 * len(nodes):
                return origin_graph, new_graph
            else:
                logging.info("Does not reach the threshold, current node number: {r}" .format(r=cur_num_nodes))
        else:
            graph = new_graph


def compare_nodes(ograph, rgraph, select, keys):
    a = []
    b = []
    for key in keys:
        a += ograph[key]
        b += rgraph[key]
    overlap = 1.0 * len(set(a).intersection(b))
    if select == 0:
        return overlap / len(b)
    elif select == 1:
        return overlap / len(a)


def calculate_graph_similarity(ograph, rgraph, nodes_to_compare=1, select=0, num_process=4):
    # methods = ("precision", "recall")

    key_o = ograph.keys()
    key_r = rgraph.keys()
    common_key = set(key_o).intersection(key_r)

    combs = combinations(common_key, nodes_to_compare)
    similarity = Parallel(n_jobs=num_process, backend="threading")(delayed(compare_nodes)(ograph, rgraph, select, key) for key in combs)
    return np.mean(similarity)


def main(in_data_path):
    pairwise_distance = read_from_file(in_data_path)
    origin_graph, random_graph = generate_random_graph(pairwise_distance)
    logging.info("Origin graph has {r} nodes" .format(r=len(origin_graph.keys())))
    logging.info("Origin graph has {r} nodes" .format(r=len(random_graph.keys())))
    print calculate_graph_similarity(origin_graph, random_graph)

if __name__ == '__main__':
    pairwise_distance_path = "data/word2vec_in_phenotypes/pairwise_distances"
    main(pairwise_distance_path)
