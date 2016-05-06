# -*- coding: utf-8 -*-
#
# parse the raw literature data, i.e., parse it.
import json
import logging
import utilities

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    )


def read_from_json(in_path):
    logging.info('Start Parsing...')
    with open(in_path + "raw/" + "pmcdoc.json", "rb") as f:
        json_data = f.readlines()
        utilities.mkdir(in_path, "parsed/")
        for data in json_data:
            tmp = json.loads(data)
            id, content = extract_clean_data(tmp)
            logging.info('Parse PMCID: ' + id)
            tmp_path = in_path + "parsed/" + id + ".json"
            if not utilities.is_file_exist(tmp_path, debug=True):
                if content != "":
                    utilities.write_to_json(content, tmp_path)


# currently, we only extract and clean basic information.(pmcid, title, body.)
def extract_clean_data(data):
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
    read_from_json(in_path)


if __name__ == '__main__':
    data_in_path = "data/"
    main(data_in_path)
