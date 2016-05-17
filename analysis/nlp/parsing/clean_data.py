# -*- coding: utf-8 -*-
#
# Clean the data, and delete invalid file
import re
import nltk
import logging
import utilities

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',)
nltk.data.path.append("/nltk")


def remove_newline(line):
    return filter(lambda x: x != "", re.split("\n", line))


def deal_with_body(body):
    sentences = nltk.sent_tokenize(body)
    compile = re.compile("\[[\d\D\s]*\]")
    new_sentences = []
    for s in sentences:
        tmp = remove_newline(s)
        if len(tmp) == 1:
            # remove strange contents, like table.
            new_sentences.append(re.sub(compile, "", tmp[0]))
    return new_sentences


def format_file(data):
    abstract = "".join(data["abstract"])
    body = "".join(data["body"])
    abstract = filter(lambda x: x != "", re.split("\n", abstract))
    body = deal_with_body(body)
    return {
        "pmc_id": data["pmc_id"],
        "abstract": abstract,
        "body": body
    }


def main(in_path):
    paths = utilities.list_files(in_path + "parsed/")
    utilities.mkdir(in_path, "parsed_all/abstract/")
    utilities.mkdir(in_path, "parsed_all/doc/")
    utilities.delete_file(in_path + "parsed_all/all_in_one")

    logging.info('Start Cleaning...')
    for p in paths:
        logging.info('Cleaning document from the following path: ' + p)
        sdata, is_valid = utilities.filter_by_file_size(p)
        if not is_valid:
            utilities.delete_file(p)
            continue
        formated = format_file(sdata)
        utilities.write_to_json(formated, p)
        # logging.info('Write document to following path...')
        utilities.append_to_smallfile(formated["abstract"], in_path + "parsed_all/abstract/")
        utilities.append_to_smallfile(formated["body"], in_path + "parsed_all/doc/")
        utilities.append_to_bigfile(p, formated["body"], in_path + "parsed_all/all_in_one")


if __name__ == '__main__':
    data_in_path = "data/"
    main(data_in_path)
