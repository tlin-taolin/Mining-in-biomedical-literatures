# -*- coding: utf-8 -*-
#

import re
import os
import sys
import pandas as pd
from info import PhenotypeInfo
sys.path.insert(0, 'util/')

import groupby as gp
import readwrite as rw
import opfiles


def read_from_csv(path):
    raw_mp_df = pd.read_csv(path)
    useful_mp_df = raw_mp_df[["PhenoID.1",
                              "Phenotype",
                              "Shown_pheno",
                              "Category"]]
    useful_mp = useful_mp_df.values.tolist()
    return useful_mp


def build_classes(lines):
    return [PhenotypeInfo(line) for line in lines]


def get_info(lines_class, v):
    return list(set([getattr(line, v) for line in lines_class]))


def summary_info(lines_class):
    categories = get_info(lines_class, "category")
    shown_phenos = get_info(lines_class, "shown_pheno")
    return categories, shown_phenos


def group_info(lines_class):
    category_ids = [(line.category, line.id) for line in lines_class]
    shownpheno_ids = [(line.shown_pheno, line.id) for line in lines_class]

    categories_grouped_ids = gp.group_by(category_ids, index=0)
    shownpheno_grouped_ids = gp.group_by(shownpheno_ids, index=0)
    return [(k, [v[1] for v in vv]) for k, vv in categories_grouped_ids], \
           [(k, [v[1] for v in vv]) for k, vv in shownpheno_grouped_ids]


def clean_blank(pheno):
    pheno = filter(lambda x: x != "", pheno.split(" "))
    return " ".join(pheno)


def clean_pheno(line):
    pheno = line.phenotype
    pattern = re.compile("(?:\[.*?\]|\(.*?\))", re.X)
    pheno = re.sub(pattern, "", pheno)
    pheno = clean_blank(pheno)
    line.phenotype = pheno
    return line


def clean_phenos(lines_class):
    return [clean_pheno(line) for line in lines_class]


def extract_line(pheno):
    return pheno.id + "\t" + pheno.phenotype + \
        "\t" + pheno.shown_pheno + "\t" + pheno.category


def write_pheno_to_file(cleaned_phenos, out_path):
    outstring = [extract_line(pheno) for pheno in cleaned_phenos]
    outstring = "\n".join(outstring)
    rw.write_to_txt(outstring, out_path, "w")


def write_groups(info):
    info_1 = "\n".join([k + "\t" + v for k, vv in info for v in vv])
    info_2 = "\n".join([k + "\t" + ",".join(vv) for k, vv in info])
    return info_1, info_2


def parsing(root):
    in_data_path = os.path.join(root, "origin", "phenotypes_id_aligner.csv")
    lines = read_from_csv(in_data_path)
    lines_class = build_classes(lines)
    categories, shown_phenos = summary_info(lines_class)
    categories_grouped_ids, shownpheno_grouped_ids = group_info(lines_class)
    cleaned_phenos = clean_phenos(lines_class)

    out_path = os.path.join(root, "cleaned_phenos")
    write_pheno_to_file(cleaned_phenos, out_path)

    out_path = os.path.join(root, "summary")
    opfiles.mkdir(out_path)
    out_path = os.path.join(root, "summary", "categories")
    rw.write_to_txt("\n".join(categories), out_path, "w")
    out_path = os.path.join(root, "summary", "shown_phenos")
    rw.write_to_txt("\n".join(shown_phenos), out_path, "w")

    out_path = os.path.join(root, "groups")
    opfiles.mkdir(out_path)
    info_1, info_2 = write_groups(categories_grouped_ids)
    out_path_1 = os.path.join(root, "groups", "categories_v1")
    out_path_2 = os.path.join(root, "groups", "categories_v2")
    rw.write_to_txt(info_1, out_path_1, "w")
    rw.write_to_txt(info_2, out_path_2, "w")
    info_1, info_2 = write_groups(shownpheno_grouped_ids)
    out_path_1 = os.path.join(root, "groups", "shown_phenos_v1")
    out_path_2 = os.path.join(root, "groups", "shown_phenos_v2")
    rw.write_to_txt(info_1, out_path_1, "w")
    rw.write_to_txt(info_2, out_path_2, "w")


if __name__ == '__main__':
    root = "data/mp"
    parsing(root)
