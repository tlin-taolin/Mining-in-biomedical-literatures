# -*- coding: utf-8 -*-
#
# Clean the data of pmcdoc, and delete invalid file
#

import sys
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',)

sys.path.insert(0, 'util/')
sys.path.insert(0, 'parsing/pmcdoc/')

import opfiles
import readwrite
import clean_data
import parse_data


def _clean_data(in_path):
    paths = opfiles.list_files(in_path + "parsed/")
    opfiles.mkdir(in_path + "parsed_all/abstract/")
    opfiles.mkdir(in_path + "parsed_all/doc/")
    opfiles.delete_file(in_path + "parsed_all/all_in_one")

    logging.info('Start Cleaning...')
    for p in paths:
        logging.info('Cleaning document from the following path: ' + p)
        sdata, is_valid = opfiles.filter_by_file_size(p, in_size=10)
        if not is_valid:
            opfiles.delete_file(p)
            continue
        formated = clean_data.format_file(sdata)
        readwrite.write_to_json(formated, p)
        # logging.info('Write document to following path...')
        to_abstract = in_path + "parsed_all/abstract/"
        to_doc = in_path + "parsed_all/doc/"
        to_all = in_path + "parsed_all/all_in_one"
        clean_data.append_to_smallfile(formated["abstract"], to_abstract)
        clean_data.append_to_smallfile(formated["body"], to_doc)
        clean_data.append_to_bigfile(p, formated["body"], to_all)


def _parse_data(in_path):
    parse_data.read_json_and_parsing(in_path)


def main(in_path):
    _parse_data(in_path)
    _clean_data(in_path)

if __name__ == '__main__':
    data_in_path = "data/"
    main(data_in_path)
