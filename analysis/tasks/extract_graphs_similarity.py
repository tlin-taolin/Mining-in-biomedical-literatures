# -*- coding: utf-8 -*-
#
# Generate a 'random' graph based on given relationship matrix
# and pre-defined rule.

import sys
import logging


sys.path.insert(0, 'graph/hp/')
sys.path.insert(0, 'graph/pmcdoc_word2vec/')

import graph_sim_basis
import build_graph
import generate_graphs
import extract_relationship_phenotype


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', )


def build_hp_graph(path):
    build_graph.extract_info_from_parsed_hp(path)
    return build_graph.extract_adjlist(path + "hp_edge_list.txt")


def build_knn_graph(path, knn, is_random):
    distances = extract_relationship_phenotype.read_from_file(path)
    if is_random:
        knn, origin = generate_graphs.generate_randomk_g(distances, knn)
    else:
        knn, origin = generate_graphs.generate_normal_g(distances, knn)
    return knn


def pipeline(hp_path, pairwisedistance_path, k_list):
    logging.info("Build Human Phenotype Graph ...")
    hp = build_hp_graph(hp_data_path)

    logging.info("Running in topK list to calculate topk graph with hp graph.")
    comparison = []
    for k in k_list:
        n_knn = build_knn_graph(pairwise_distance_path, knn=k, is_random=False)
        logging.info("get similarity list between n_knn and hp...")
        n_sim_list = graph_sim_basis.get_graph_simlist(hp, n_knn)
        logging.info("get similarity between n_knn and hp...")
        n_sim = graph_sim_basis.get_graph_sim(n_sim_list)

        r_knn = build_knn_graph(pairwise_distance_path, knn=k, is_random=True)
        logging.info("get similarity list between n_knn and hp...")
        r_sim_list = graph_sim_basis.get_graph_simlist(hp, r_knn)
        logging.info("get similarity between n_knn and hp...")
        r_sim = graph_sim_basis.get_graph_sim(r_sim_list)
        comparison.append((n_sim, r_sim))
    return comparison


def debug(hp_data_path, pairwise_distance_path):
    logging.info("Build Human Phenotype Graph ...")
    hp_graph = build_hp_graph(hp_data_path)
    logging.info("Build non-random KNN PMC Graph ...")
    knn_graph = build_knn_graph(pairwise_distance_path, knn=3, is_random=False)
    logging.info("Get similarity list between two graphs ...")
    sim_list = graph_sim_basis.get_graph_simlist(hp_graph, knn_graph)
    logging.info("Get similarity between two graphs ...")
    sim = graph_sim_basis.get_graph_sim(sim_list)
    logging.info("The Similarity between two graphs is {r}".format(r=sim))

    logging.info("Build random KNN PMC Graph ...")
    knn_graph = build_knn_graph(pairwise_distance_path, knn=3, is_random=True)
    logging.info("Get similarity list between two graphs ...")
    sim_list = graph_sim_basis.get_graph_simlist(hp_graph, knn_graph)
    logging.info("Get similarity between two graphs ...")
    sim = graph_sim_basis.get_graph_sim(sim_list)
    logging.info("The Similarity between two graphs is {r}".format(r=sim))


if __name__ == '__main__':
    hp_data_path = "data/hp/"
    pairwise_distance_path = "data/word2vec_in_phenotypes/pairwise_distances"
    debug(hp_data_path, pairwise_distance_path)
