# -*- coding: utf-8 -*-
#
# analysis the combination of word2vec in phenotype
import math
import logging
import utilities
import numpy as np
from itertools import product
from collections import deque
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
    return [ind.strip("\n").split("::")[1].split(" ") for ind in in_data]


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


def extract_potential_index(phases):
    id_map_isa = {}
    name_map_id = {}
    id_pairs = set()
    waiting = deque([])
    phenotype_path = "../phenotype_graph/data/parsed_hp"
    with open(phenotype_path, "r") as o:
        lines = o.readlines()
    for line in lines:
        elements = line.split("::")
        id = elements[0]
        name = elements[1]
        isa = elements[4].strip("\n").split(",")
        id_map_isa[id] = isa
        # corner case: there exists phenotype with the same name
        # but with different id and definiation.
        name_map_id[name] = id

    map_name_to_ids = lambda name: name_map_id[name]

    names = list(name_map_id.keys())
    ids = name_map_id.values()
    map_id_to_ind = lambda id: phases.index(names[ids.index(id)])

    for phase in phases:
        id = map_name_to_ids(phase)
        isas = id_map_isa[id]
        for isa in isas:
            if isa != "":
                id_pairs.add((id, isa))
                waiting.append((id, isa))

    logging.info("Generate some meaningful pairs (id)...")
    while len(waiting):
        left, right = waiting.pop()
        if right == "":
            continue
        for id in id_map_isa[right]:
            ntuple = (left, id)
            if ntuple not in id_pairs:
                id_pairs.add(ntuple)
                waiting.append(ntuple)
    id_pairs = list(id_pairs)

    logging.info("Generate {r} raw pairs (ind)..." .format(r=len(id_pairs)))
    index_pairs = []
    for pair in id_pairs:
        if pair[1] == "":
            continue
        try:
            tmp = (map_id_to_ind(pair[0]), map_id_to_ind(pair[1]))
            index_pairs.append(tmp)
        except:
            pass

    logging.info("Generate {r} pairs (ind)..." .format(r=len(index_pairs)))
    return index_pairs


def generate_pairs(phase_list):
    logging.info("Generate pairs ...")
    indexs = xrange(0, len(phase_list))
    return [(ind1, ind2) for ind1 in indexs for ind2 in indexs if ind1 < ind2]


def cal_euclidean_distance(phases_dict, keys, i, j):
    n_i = keys[i]
    n_j = keys[j]
    v1 = phases_dict[n_i]
    v2 = phases_dict[n_j]
    logging.info("Calculate the distance between <" + n_i + "> and <" + n_j + "> ...")
    diff = v1 - v2
    distance = np.dot(diff.T, diff)
    return n_i, n_j, str(math.sqrt(distance))


def cal_pairwise_distance_by_thread(phases_dict, index_pairs, num_process=4):
    keys = list(phases_dict.keys())
    logging.info("Calculate pairwise distance, existing " + str(len(index_pairs)) + " pairs ...")
    return Parallel(n_jobs=num_process, backend="threading")(delayed(
        cal_euclidean_distance)(phases_dict, keys, i, j) for i, j in index_pairs)


def write_pairwise_distance_to_file(pairwise_distance, out_path):
    out = ""
    for x in pairwise_distance:
        out += x[0] + "\t" + x[1] + "\t" + x[2] + "\n"
        out += x[1] + "\t" + x[0] + "\t" + x[2] + "\n"
    with open(out_path, "w") as f:
        f.write(out)


def main(model_path, phenotype_path, distances_pairs_path):
    model_pairs = load_models(model_path)
    best_model = find_best_model(model_pairs)
    word_model = load_model(best_model)
    phenotypes = parse_phenotype(phenotype_path)
    words_dict = map_word2vec_to_dict(word_model, phenotypes)
    phases_dict = map_phases_to_vec(words_dict, phenotypes)
    phases = list(phases_dict.keys())
    # index_pairs = generate_pairs(phases)
    index_pairs = extract_potential_index(phases)
    distances = cal_pairwise_distance_by_thread(phases_dict, index_pairs, 5)
    write_pairwise_distance_to_file(distances, distances_pairs_path)


if __name__ == '__main__':
    model_path = "model/"
    phenotype_path = "../phenotype_graph/data/parsed_hp"
    distances_pairs_path = "data/word2vec_in_phenotypes/pairwise_distances"
    main(model_path, phenotype_path, distances_pairs_path)
