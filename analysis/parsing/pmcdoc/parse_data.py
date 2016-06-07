# -*- coding: utf-8 -*-
#
# parse the raw literature data, i.e., parse it.
import sys
import json
import logging

sys.path.insert(0, 'util/')
import opfiles

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',)


def read_json_and_parsing(in_path):
    to_be_parse = in_path + "raw/" + "pmcdoc.json"

    logging.info('Start Parsing...')
    with open(to_be_parse, "rb") as f:
        logging.info('Build/rebuild parsing folder...')
        opfiles.mkdir(in_path + "parsed/")

        json_data = f.readlines()
        for data in json_data:
            tmp = json.loads(data)
            id, content = extract_cleandata(tmp)
            logging.info('Parse PMCID: ' + id)
            tmp_path = in_path + "parsed/" + id + ".json"
            if not opfiles.is_file_exist(tmp_path, debug=True):
                if content != "":
                    opfiles.write_to_json(content, tmp_path)


# currently, we only extract and clean basic information.(pmcid, title, body.)
def extract_cleandata(data):
    if data["body"] == None:
        return data["pmc_id"], ""
    else:
        abstract = data["abstract"]
        body = data["body"]
        if len(abstract) != "" or len(body) != "":
            return data["pmc_id"], data
        else:
            return data["pmc_id"], ""


def main(in_path):
    read_json_and_parsing(in_path)


if __name__ == '__main__':
    data_in_path = "data/"
    main(data_in_path)
