# -*- coding: utf-8 -*-
#
# Generate a 'random' graph based on given relationship matrix
# and pre-defined rule.

import logging
import numpy as np
from itertools import combinations
from joblib import Parallel, delayed
import generate_random_graph
import extract_relationship_phenotype

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', )


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
    pairwise_distance = extract_relationship_phenotype.read_from_file(in_data_path)
    origin_graph, random_graph = generate_random_graph.graph_generation_naive(pairwise_distance)
    logging.info("Origin graph has {r} nodes" .format(r=len(origin_graph.keys())))
    logging.info("Origin graph has {r} nodes" .format(r=len(random_graph.keys())))
    print calculate_graph_similarity(origin_graph, random_graph)

if __name__ == '__main__':
    pairwise_distance_path = "data/word2vec_in_phenotypes/pairwise_distances"
    main(pairwise_distance_path)
