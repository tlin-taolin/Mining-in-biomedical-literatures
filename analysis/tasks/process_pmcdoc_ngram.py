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
import analyze_graph


def pipeline():
    logging.info("Clean raw dataset, and merge them to a single file...")
    clean_rawdata._clean()
    logging.info("Analyze the result by graph...")
    analyze_graph._analysis()


if __name__ == '__main__':
    pipeline()
