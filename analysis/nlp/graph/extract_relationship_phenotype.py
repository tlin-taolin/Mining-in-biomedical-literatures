# -*- coding: utf-8 -*-
#
# Extract the relationship information of each phenotype.

import pickle
import logging
import numpy as np
import scipy.sparse as sp
import pandas as pd
from itertools import groupby


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', )


# without pandas
def read_from_file(path):
    logging.info("Read data from file ...")
    with open(path, "r") as f:
        files = f.readlines()
    return map(lambda x: x.strip("\n").split("\t"), files)


def select_topk(pairwise, groupby_index=0, topk=10):
    logging.info("Select topk from pairwise based on its phenotype.")
    sorted_pairwise = sorted(pairwise, key=lambda x: x[groupby_index])
    topk_dict = {}
    group_list = []
    for key, group in groupby(sorted_pairwise, lambda x: x[groupby_index]):
        tmp = []
        for element in group:
            tmp.append((element[1], float(element[4])))
        topk_dict[key] = sorted(tmp, key=lambda x: x[1], reverse=False)[0:topk-1]
        group_list.append([key, tmp])
    return topk_dict, group_list


def write_topK_to_file(topk_dict, out_path):
    logging.info("Write the selected topK to the file...")
    out_str = ""
    for key, value in topk_dict.items():
        out_str += key + ":" + ";".join(map(lambda x: x[0] + "," + str(x[1]), value)) + "\n"
    with open(out_path, "w") as out:
        out.write(out_str)


def build_matrix(group_list):
    logging.info("Build matrix without pandas...")
    phenotype_indices = {}
    num_of_phenotype = len(group_list)
    for i in range(num_of_phenotype):
        phenotype_indices[group_list[i][0]] = i
    matrix = sp.lil_matrix((num_of_phenotype, num_of_phenotype))
    for pheno1, pairs in group_list:
        pheno1_index = phenotype_indices[pheno1]
        for pheno2, score in pairs:
            pheno2_index = phenotype_indices[pheno2]
            matrix[pheno1_index, pheno2_index] = score
    return matrix


def save_matrix_to_file(matrix, path):
    logging.info("save the matrix to the path...")
    with open(path, 'wb') as handle:
        pickle.dump(matrix, handle)


def main_without_pandas(in_data_path, out_knn_path, out_matrix_path):
    pairwise_distance = read_from_file(in_data_path)
    topk_dict, group_list = select_topk(pairwise_distance)
    write_topK_to_file(topk_dict, out_knn_path)
    matrix = build_matrix(group_list)
    save_matrix_to_file(matrix, out_matrix_path)


# with pandas
def read_from_file_through_pandas(in_data_path):
    logging.info("Read data from file through pandas ...")
    m = pd.read_table(in_data_path, sep="\t", header=None)
    return m


def build_matrix_through_pandas(data_file):
    logging.info("Build matrix with pandas...")
    phenotypes = np.unique(data_file[2])
    num_of_phenotype = len(phenotypes)
    phenotype_indices = {}

    for i in range(num_of_phenotype):
        phenotype_indices[phenotypes[i]] = i

    matrix = sp.lil_matrix((num_of_phenotype, num_of_phenotype))
    for (id1, id2, p1, p2, score) in data_file.values:
        matrix[phenotype_indices[p1], phenotype_indices[p2]] = float(score)
    return matrix


def select_topk_through_pandas(data_file, topk=10):
    logging.info("Select topk from pairwise based on its phenotype through pandas...")
    df = pd.DataFrame(data_file).copy()
    df.columns = ['id1', 'id2', 'p1', 'p2', 'score']
    return df.groupby('p1').head(topk)


def main_with_pandas(in_data_path, out_knn_path, out_matrix_path):
    data_file = read_from_file_through_pandas(in_data_path)
    select_topk_through_pandas(data_file)
    matrix = build_matrix_through_pandas(data_file)
    save_matrix_to_file(matrix, out_matrix_path)


if __name__ == '__main__':
    pairwise_distance_path = "data/word2vec_in_phenotypes/pairwise_distances"
    out_knn_path = "data/word2vec_in_phenotypes/phenotype_knn"
    out_matrix_path = "data/word2vec_in_phenotypes/phenotype_matrix.pickle"
    main_without_pandas(pairwise_distance_path, out_knn_path, out_matrix_path)
    main_with_pandas(pairwise_distance_path, out_knn_path, out_matrix_path)
