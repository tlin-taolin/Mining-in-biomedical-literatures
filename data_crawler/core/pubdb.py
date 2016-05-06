# -*- coding: utf-8 -*-
#
# pubmed pipeline
#

from pymongo import MongoClient, ASCENDING
from settings.parameters import *


def init_collection():
    client = MongoClient(DATABASE_LOCATION, DATABASE_PORT)
    db = client.crawl
    summary = db.summary
    pmcdoc = db.pmcdoc
    if MODE:
        destroy_collection(summary)
        destroy_collection(pmcdoc)
    summary.create_index([("pubmed_id", ASCENDING)], unique=True)
    pmcdoc.create_index([("pmc_id", ASCENDING), ("pubmed_id", ASCENDING)], unique=True)
    return summary, pmcdoc

def destroy_collection(collection):
    collection.drop()

def build_doc_from_template(temp, in_dict):
    template = dict(temp)
    for key, value in in_dict.items():
        if type(template[key]) == list and type(value) != list:
            template[key] = template[key] + [value,]
        else:
            template[key] = value
    return template
