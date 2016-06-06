# -*- coding: utf-8 -*-
#
# Clean the data of pmcdoc, and delete invalid file
#

import sys
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',)

sys.path.insert(0, 'util/')
sys.path.insert(0, 'graph/pmcdoc_ngram/')

import clean_rawdata
import its_analysis


def pipeline():
    level = ["ngram-doc-level/", "ngram-sent-level/"][1]
    logging.info("Clean raw dataset of {}, and merge them to a single file...".
                 format(level))
    clean_rawdata.cleaning(level)
    logging.info("Analyze the result by graph...")
    its_analysis.analysis(level)


if __name__ == '__main__':
    pipeline()
