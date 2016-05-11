# -*- coding: utf-8 -*-
#
# Do the statistics for the parsed results.

from parse_hp import *
import nltk
import re

nltk.data.path.append("/nltk")


def split_names(names):
    return [re.split("\s", name) for name in names]


def stat_names(names):
    splitted_name = split_names(names)
    num_of_names = len(splitted_name)
    len_of_names = [len(name) for name in splitted_name]
    min_len_of_names = min(len_of_names)
    max_len_of_names = max(len_of_names)
    average_len_of_names = 1.0 * sum(len_of_names) / num_of_names
    return min_len_of_names, max_len_of_names, average_len_of_names


def build_name_tokens(names):
    stopwords = nltk.corpus.stopwords.words('english')

    tokens = []
    for words in names:
        tokens += [word.lower().strip() for word in nltk.word_tokenize(words) if word.lower() not in stopwords]
    return sorted(set(tokens))


def get_nouns(name_tokens):
    tagged_token = nltk.pos_tag(name_tokens)
    return [word for word, tag in tagged_token if tag == "NN"]


def output_name_tokens(file_name, tokens):
    with open("../data/" + file_name, "a") as w:
        tmp = "\n".join(tokens)
        out = re.sub(r"\d+", "", tmp)
        if out is not "":
            w.write(tmp)


if __name__ == '__main__':
    path = "data/graph/humanphenotype.obo"
    out_path = "data/graph/parsed_hp"
    lines = read_data(path)
    cleaned_lines = clean_data(lines)
    parsed_lines = parsing(cleaned_lines)
    nodes = build_nodes(parsed_lines)
    names = extract_names(nodes)
    name_tokens = build_name_tokens(names)
    # output_name_tokens("1gram_name_tokens", name_tokens)
    # output_name_tokens("ngram_name_tokens", names)
    noun_tokens = get_nouns(name_tokens)
    output_name_tokens("1gram_noun_tokens", noun_tokens)
