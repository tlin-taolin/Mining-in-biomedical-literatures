# -*- coding: utf-8 -*-

import os
import sys
import nltk
import logging
from nltk.stem import WordNetLemmatizer

sys.path.insert(0, 'util/')
import opfiles
import readwrite as rw


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',)


def define_human_synonym():
    return None


def define_mouse_synonym():
    return None


def take_nn_words(data, wordnet_lemmatizer):
    tagged = set()
    for da in data:
        words = nltk.word_tokenize(da.lower())
        words = [wordnet_lemmatizer.lemmatize(word) for word in words]
        tagged_words = nltk.pos_tag(words)
        for w in tagged_words:
            if "NN" in w[1]:
                tagged.add(w[0])
    return tagged


def classify_by_nouns(nouns):
    pass


def read_json_and_classify(in_path):
    file_paths = opfiles.list_files(os.path.join(in_path, "parsed/"))
    out_root_path = os.path.abspath(os.path.join(in_path, "classified/"))

    logging.info('Start Classify...')
    wordnet_lemmatizer = WordNetLemmatizer()

    for p in file_paths:
        logging.info('Classify the document of the following path: ' + p)
        sdata = rw.read_from_json(p)
        nouns = take_nn_words(sdata["abstract"], wordnet_lemmatizer)


def main(in_path):
    read_json_and_classify(in_path)


if __name__ == '__main__':
    in_path = "data/"
    main(in_path)
