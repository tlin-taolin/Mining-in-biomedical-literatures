# -*- coding: utf-8 -*-
#
# analysis the combination of word2vec in phenotype
import math
import logging
import utilities
import numpy as np
from itertools import product
from gensim.models import word2vec
from joblib import Parallel, delayed

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', )


def load_models(model_root_path):
    logging.info("Load word2ver models...")
    model_paths = utilities.list_files(model_root_path)
    model_paths = get_valid_models(model_paths)
    models = [(model, load_model(model)) for model in model_paths]
    return models


def load_model(path):
    return word2vec.Word2Vec.load(path)


def get_valid_models(model_paths):
    return filter(lambda x: ".npy" not in x, model_paths)


def find_best_model(name_model_pairs):
    for name, model in name_model_pairs:
        pass
    best_model = name_model_pairs[0][0]
    logging.info("The best model is " + best_model)
    return best_model


def parse_phenotype(path):
    logging.info("Parse phenotypes...")
    with open(path, "r") as f:
        in_data = f.readlines()
    return [ind.strip("\n").split(" ") for ind in in_data]


def map_phases_to_vec(phase_dict, phases):
    logging.info("Map each phase to a word2vec...")
    phases_dict = dict()
    for phase in phases:
        name = " ".join(phase)
        words_word2vec = map(lambda word: phase_dict[word], phase)
        phase_word2vec = reduce(lambda a, b: a + b, words_word2vec)
        phases_dict[name] = phase_word2vec
    return phases_dict


def map_word2vec_to_dict(model, phases, dim=500):
    logging.info("Find the unique word for phenotype")
    my_dict = dict()
    for phase in phases:
        for word in phase:
            if word not in my_dict:
                my_dict[word] = map_word_to_vec(model, word, dim)
    return my_dict


def map_word_to_vec(model, word, dim):
    try:
        vec = model[word]
    except:
        vec = np.zeros(dim)
    return vec


def cal_euclidean_distance(pairs, i, j):
    logging.info("Calculate the distance between <" + i + "> and <" + j + "> ...")
    v1 = pairs[i]
    v2 = pairs[j]
    diff = v1 - v2
    distance = np.dot(diff, diff.T)
    return i, j, str(math.sqrt(distance))


def cal_pairwise_distance(pairs, num_process=4):
    keys = pairs.keys()
    logging.info("Calculate pairwise distance, existing " + str(len(keys)) + " keys ...")
    return Parallel(n_jobs=num_process, backend="threading")(delayed(
        cal_euclidean_distance)(pairs, i, j) for i, j in product(keys, keys))


def write_pairwise_distance_to_file(pairwise_distance, out_path):
    out = "\n".join(map(lambda x: "\t".join(x), pairwise_distance))
    with open(out_path, "w") as f:
        f.write(out)


def main(model_path, phenotype_path, distances_pairs_path):
    model_pairs = load_models(model_path)
    best_model = find_best_model(model_pairs)
    word_model = load_model(best_model)
    phenotypes = parse_phenotype(phenotype_path)
    words_dict = map_word2vec_to_dict(word_model, phenotypes)
    phases_dict = map_phases_to_vec(words_dict, phenotypes)
    distances = cal_pairwise_distance(phases_dict, 8)
    write_pairwise_distance_to_file(distances, distances_pairs_path)

if __name__ == '__main__':
    model_path = "model/"
    phenotype_path = "../phenotype_graph/data/ngram_name_tokens"
    distances_pairs_path = "data/distance_of_phenotypes_pairs/distances"
    main(model_path, phenotype_path, distances_pairs_path)
