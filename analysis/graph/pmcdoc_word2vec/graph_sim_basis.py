# -*- coding: utf-8 -*-
#
# calculate the basis similarity between two graphs.

import numpy as np
from joblib import Parallel, delayed


def get_node_sim(ograph, rgraph, node):
    """Return a tuple: (precision, recall)"""
    o_edge_nodes = ograph[node]
    r_edge_nodes = rgraph[node]
    overlap = 1.0 * len(set(o_edge_nodes).intersection(r_edge_nodes))
    return overlap / len(r_edge_nodes), overlap / len(o_edge_nodes)


def get_graph_simlist(ograph, rgraph, num_process=4):
    o_nodes = ograph.keys()
    r_nodes = rgraph.keys()
    nodes = set(o_nodes).intersection(r_nodes)

    similarity = Parallel(n_jobs=num_process, backend="threading")(delayed(get_node_sim)(ograph, rgraph, node) for node in nodes)
    return similarity


def get_graph_sim(sims):
    len_of_sims = len(sims)
    sum_sim = reduce(lambda a, b: (a[0] + b[0], a[1] + b[1]), sims)
    return np.array(sum_sim) / len_of_sims
