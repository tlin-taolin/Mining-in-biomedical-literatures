# -*- coding: utf-8 -*-
#
#
import sys
sys.path.insert(0, 'graph/pmcdoc_word2vec/')
sys.path.insert(0, 'util/')

import opfiles
import extract_doc_feature


def training_different_word2vec_model(paths, num_thread):
    for num_of_features in [500, 900, 2000, 3000]:
        for negative in [0, 5, 11, 17, 20]:
            for size_content in [4, 6, 8, 10]:
                model, model_name = extract_doc_feature.extract_word2vec(paths, toExtract="abstract",\
                                    num_workers=num_thread, negative_sampling=negative,\
                                    context=size_content)
                model.save(model_name)


if __name__ == '__main__':
    in_path = "data/parsed/"
    paths = opfiles.list_files(in_path)
    training_different_word2vec_model(paths, num_thread=4)
