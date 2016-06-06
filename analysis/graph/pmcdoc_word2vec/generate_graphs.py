# -*- coding: utf-8 -*-
#
# Generate a 'random' graph based on given relationship matrix
# and pre-defined rule.

import sys
import copy
import logging
from random import seed, sample
import extract_relationship_phenotype

sys.path.insert(0, 'util/')

import is_directed_graph_cyclic


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', )


def prepare_for_generation(distances, top, is_random, inseed=6666666):
    seed(inseed)
    knn_dict, group_list = extract_relationship_phenotype.select_topk(distances, top, is_random)

    nodes = knn_dict.keys()
    knn_graph = dict([(key, map(lambda x: x[0], value)) for key, value in knn_dict.items()])
    origin_graph = dict([(value[0], map(lambda x: x[0], value[1])) for value in group_list])
    return nodes, knn_graph, origin_graph


def generate_naive_g(distances, top, inseed=6666666):
    nodes, knn_graph, origin_graph = prepare_for_generation(distances, top, inseed)
    total_num_nodes = len(nodes)
    random_pick_node = lambda x: sample(nodes, 1)[0]
    random_pick_node_neighbor = lambda x: sample(knn_graph[x], 1)[0]

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
            if cur_num_nodes > 3.0 / 5 * total_num_nodes:
                return origin_graph, new_graph
            else:
                logging.debug("Does not reach the threshold.\nCurrent node number:{r}. Total node number:{t}." .format(r=cur_num_nodes, t=total_num_nodes))
        else:
            graph = new_graph


def generate_normal_g(distances, top, inseed=6666666):
    nodes, knn_graph, origin_graph = prepare_for_generation(distances, top, False, inseed)
    return knn_graph, origin_graph


def generate_randomk_g(distances, top, inseed=6666666):
    nodes, knn_graph, origin_graph = prepare_for_generation(distances, top, True, inseed)
    return knn_graph, origin_graph


def debug(in_data_path):
    topk = 5
    distances = extract_relationship_phenotype.read_from_file(in_data_path)
    generate_naive_g(distances, False, topk)


if __name__ == '__main__':
    in_data_path = "data/word2vec_in_phenotypes/pairwise_distances"
    debug(in_data_path)
