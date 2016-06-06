# -*- coding: utf-8 -*-
#
import sys
import logging
import numpy as np
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.cluster import KMeans
from sklearn.preprocessing import scale
import calculate_distance_of_word2vecs as cw
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from joblib import Parallel, delayed


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', )


def load_model(model_path):
    model_pairs = cw.load_models(model_path)
    best_model = cw.find_best_model(model_pairs)
    word_model = cw.load_model(best_model)
    return word_model


def load_worddict(word_model):
    id_map_isa, id_map_phase, phase_map_id, words_list = cw.parse_phenotype(phenotype_path)
    words_dict = cw.map_word2vec_to_dict(word_model, words_list)
    word2vec_dict = cw.map_phases_to_vec(words_dict, words_list)
    return id_map_isa, id_map_phase, phase_map_id, word2vec_dict


def cal_diff(phases_dict, info):
    phase1 = info[2]
    phase2 = info[3]
    v1 = phases_dict[phase1]
    v2 = phases_dict[phase2]
    return v1 - v2


def calculate_diff(phase_dict, id_pairs, num_process=4):
    return Parallel(n_jobs=num_process, backend="threading")(delayed(
        cal_diff)(phase_dict, info) for info in id_pairs)


def generate_pairs(id_map_isa, id_map_phase, phase_map_id):
    pairs = cw.extract_potential_index(id_map_isa, id_map_phase, phase_map_id)
    # pairs = cw.extract_pairs(id_map_phase, phase_map_id)
    return pairs


def prepare_kmeans(diffs):
    ndiffs = np.array(diffs)
    return scale(ndiffs)


def run_kmeans(ndiffs, num_cluster):
    estimator = KMeans(init='k-means++', n_clusters=num_cluster, n_init=10)
    estimator.fit(ndiffs)
    return estimator


def visualize_kmeans(estimator):
    pass


def debug(model_path, phenotype_path):
    model = load_model(model_path)
    id_map_isa, id_map_phase, phase_map_id, phase_dict = load_worddict(model)
    pairs = generate_pairs(id_map_isa, id_map_phase, phase_map_id)
    ndiffs = calculate_diff(phase_dict, pairs, num_process=6)
    diffs = prepare_kmeans(ndiffs)
    estimator = run_kmeans(diffs, num_cluster=10)
    estimated = estimator.predict(diffs)
    transformed = estimator.transform(diffs)
    # print estimated
    print transformed

if __name__ == '__main__':
    model_path = "data/model/"
    phenotype_path = "data/hp/parsed_hp"
    debug(model_path, phenotype_path)
