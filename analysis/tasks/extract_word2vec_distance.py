# -*- coding: utf-8 -*-
#
# Extract the relationship information of each phenotype.
#
import sys

sys.path.insert(0, 'graph/pmcdoc_word2vec/')

import calculate_distance_of_word2vecs
import extract_relationship_phenotype

if __name__ == '__main__':
    model_path = "data/model/"
    phenotype_path = "data/graph/parsed_hp"
    distances_pairs_path = "data/word2vec_in_phenotypes/pairwise_distances"
    calculate_distance_of_word2vecs.calculate_word2vec_distences(model_path, phenotype_path, distances_pairs_path)

    pairwise_distance_path = "data/word2vec_in_phenotypes/pairwise_distances"
    out_knn_path = "data/word2vec_in_phenotypes/phenotype_knn"
    out_matrix_path = "data/word2vec_in_phenotypes/phenotype_matrix.pickle"
    extract_relationship_phenotype.main_without_pandas(pairwise_distance_path, out_knn_path, out_matrix_path)
