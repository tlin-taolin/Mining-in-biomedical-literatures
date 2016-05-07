# -*- coding: utf-8 -*-
#
# classify the document based on the feature/subject of the experiement.
import nltk
import logging
import utilities
from gensim.models import word2vec

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',)
nltk.data.path.append("/nltk")


def load_model(model_path="model/"):
    logging.info("Load word2ver model")
    models = utilities.list_files(model_path)
    model_scores = []
    for m in models:
        model = word2vec.Word2Vec.load(m)
        score = evaluate_word2vec_model(model)
        model_scores.append([m, score])
    best_model = sorted(model_scores, key=lambda x: x[1])[0][0]
    return word2vec.Word2Vec.load(best_model)


def evaluate_word2vec_model(model):
    # evaluate the quality and accuracy of the model.
    # for a score, the smaller, the better.
    pass


def classify_data(paths):
    logging.info("Start: classifiying the dataset")
    pass


def main(in_path):
    paths = utilities.list_files(in_path)
    classify_data(paths)


if __name__ == '__main__':
    data_in_path = "data/"
    main(data_in_path)
