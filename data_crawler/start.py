# -*- coding: utf-8 -*-
#
# A pipeline for web crawler
#

# import package
import re
import os
from core import Logger


def init(path):
    os.system("rm -rf " + path + "logs/history.log")


def get_batch_cmd(path, term):
    return "python " + path + "start_crawler.py -d pubmed -t " + term + " -a 500 -c 6 -p 4"


def run_batch_cmds(path, terms):
    for term in terms:
        cmd = get_batch_cmd(path, term)
        os.system(cmd)


def main(path, terms):
    logger = Logger.get_logger('Main')
    logger.info("START THE SYSTEM!")
    init(path)
    run_batch_cmds(path, terms)


def build_search_terms():
    with open("db/parsed_name", "r") as open_term:
        terms = open_term.readlines()
    search_terms = []
    for term in terms:
        tmp = re.split("\s", term.strip("\n"))
        search_terms.append("+".join(tmp))
    return search_terms


# Main entry
if __name__ == '__main__':
    project_path = "/home/tlin/notebooks/"
    terms = build_search_terms()
    main(project_path, terms)
