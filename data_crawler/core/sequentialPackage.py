# -*- coding: utf-8 -*-
#
# a sequential worker
#

import time
from settings.parameters import *
from pubId import PubmedId
from pubsummary import PubmedSummary
from pubdoc import PubmedDoc


def get_pubmed_ids(option):
    return PubmedId(option).search_id_list(debug=MODE)


def get_npubmed_ids(pubmed_ids, summary):
    # if the token pubmed_id has already included in the collection summary.
    # ignore it, otherwise return the pubmed_id.
    projection = [s["pubmed_id"] for s in summary.find(projection={"pubmed_id": True})]
    return list(set(pubmed_ids) - set(projection))


def get_update_summary(pubmed_ids, summary, db):
    ps = PubmedSummary()
    summary_docs = []

    for pid in pubmed_ids:
        tmp = ps.get_summary(db, pid)
        summary_docs.append(tmp)
        time.sleep(DOWNLOAD_DELAY)
    if summary_docs:
        summary.insert_many(summary_docs)


def get_npmc_id(summary, pmcdoc):
    got_pmc_id = [s["pmc_id"] for s in summary.find({"pmc_id": {"$ne": ""}})]
    parsed_pmc_id = [s["pmc_id"] for s in pmcdoc.find()]
    return list(set(got_pmc_id) - set(parsed_pmc_id))


def get_pmc_doc(pmc_ids, pmcdoc):
    doc = PubmedDoc()
    pmc_docs = []

    for pmc_id in pmc_ids:
        tmp = doc.search_pmc(pmc_id)
        if tmp is not None:
            pmc_docs.append(tmp)
        time.sleep(DOWNLOAD_DELAY)
    if pmc_docs:
        pmcdoc.insert_many(pmc_docs)
