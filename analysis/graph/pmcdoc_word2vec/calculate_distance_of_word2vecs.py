# -*- coding: utf-8 -*-
#
# analysis the combination of word2vec in phenotype
import sys
import math
import logging
import numpy as np
from collections import deque
from gensim.models import word2vec
from joblib import Parallel, delayed

sys.path.insert(0, 'util/')
import readwrite
import opfiles

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', )


def load_models(model_root_path):
    logging.info("Load word2ver models...")
    model_paths = opfiles.list_files(model_root_path)
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

    lines = readwrite.read_from_txt(path)

    id_map_isa = {}
    id_map_phase = {}
    phase_map_id = {}
    words_list = []

    for line in lines:
        elements = line.strip("\n").split("::")
        id = elements[0]
        phase = elements[1]
        words = phase.split(" ")
        isa = elements[4].split(",")
        id_map_isa[id] = isa
        id_map_phase[id] = phase
        words_list.append(words)
        # corner case: there exists phenotype with the same name
        # but with different id and definiation.
        phase_map_id[phase] = id

    return id_map_isa, id_map_phase, phase_map_id, words_list


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


def extract_potential_index(id_map_isa, id_map_phase, phase_map_id):

    id_pairs = set()
    waiting = deque([])
    phases = list(phase_map_id.keys())
    map_phase_to_ids = lambda phase: phase_map_id[phase]
    map_id_phase = lambda id: id_map_phase[id]

    for phase in phases:
        id = map_phase_to_ids(phase)
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
    raw_id_pairs = list(id_pairs)

    logging.info("Generate {r} raw pairs (ind)..." .format(r=len(raw_id_pairs)))
    id_pairs = []
    for pair in raw_id_pairs:
        if pair[1] == "":
            continue
        try:
            tmp = pair + (map_id_phase(pair[0]), map_id_phase(pair[1]))
            id_pairs.append(tmp)
        except:
            pass
    logging.info("Generate {r} pairs (ind)..." .format(r=len(id_pairs)))
    return id_pairs


def generate_pairs(phase_map_id, id_map_phase):
    logging.info("Generate complete pairs ...")
    ids = phase_map_id.values()
    pairs = []
    for ind1, id1 in enumerate(ids):
        for ind2, id2 in enumerate(ids):
            if ind1 <= ind2:
                pairs.append((id1, id2, id_map_phase[id1], id_map_phase[id2]))
    return pairs


def cal_euclidean_distance(phases_dict, info):
    phase1 = info[2]
    phase2 = info[3]
    v1 = phases_dict[phase1]
    v2 = phases_dict[phase2]
    logging.debug("Calculate the distance between <" + phase1 + "> and <" + phase2 + "> ...")
    diff = v1 - v2
    distance = np.dot(diff.T, diff)
    return info[0], info[1], phase1, phase2, str(math.sqrt(distance))


def cal_pairwise_distance_by_thread(phases_dict, id_pairs, num_process=4):
    logging.info("Calculate pairwise distance, existing "+str(len(id_pairs))+" pairs ...")
    return Parallel(n_jobs=num_process, backend="threading")(delayed(
        cal_euclidean_distance)(phases_dict, info) for info in id_pairs)


def write_pairwise_distance_to_file(pairwise_distance, out_path):
    out = ""
    for x in pairwise_distance:
        out += x[0]+"\t"+x[1]+"\t"+x[2]+"\t"+x[3]+"\t"+x[4]+"\n"
        out += x[1]+"\t"+x[0]+"\t"+x[3]+"\t"+x[2]+"\t"+x[4]+"\n"
    readwrite.write_to_txt(out, out_path)


def calculate_word2vec_distences(model_path, phenotype_path, distances_pairs_path):
    model_pairs = load_models(model_path)
    best_model = find_best_model(model_pairs)
    word_model = load_model(best_model)
    id_map_isa, id_map_phase, phase_map_id, words_list = parse_phenotype(phenotype_path)
    words_dict = map_word2vec_to_dict(word_model, words_list)
    phases_dict = map_phases_to_vec(words_dict, words_list)
    # id_pairs = generate_pairs(phase_map_id, id_map_phase)
    id_pairs = extract_potential_index(id_map_isa, id_map_phase, phase_map_id)
    distances = cal_pairwise_distance_by_thread(phases_dict, id_pairs, 5)
    write_pairwise_distance_to_file(distances, distances_pairs_path)


if __name__ == '__main__':
    model_path = "data/model/"
    phenotype_path = "data/graph/parsed_hp"
    distances_pairs_path = "data/word2vec_in_phenotypes/pairwise_distances"
    calculate_word2vec_distences(model_path, phenotype_path, distances_pairs_path)
