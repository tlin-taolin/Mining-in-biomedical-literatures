# -*- coding: utf-8 -*-
#
# pubmed pipeline
#

import utils
import pubdb
import sequentialPackage
import parallelPackage
from logger import Logger
from pubId import PubmedId
from pubsummary import PubmedSummary
from pubdoc import PubmedDoc
from settings.parameters import *

class PubMed(object):
    def __init__(self, arg):
        super(PubMed, self).__init__()
        self.logger = Logger.get_logger(utils.get_fullname(self))
        self.logger.info("Initialize the crawler for pubmed.")
        self.option = arg
        self.is_valid()

    def is_valid(self):
        if not (bool(self.option.term) or bool(self.option.pid)):
            self.logger.error("Input argument is not correct!")
            quit()

    def get_work_mode(self):
        if self.option.choice == 0:
            return "crawl pubmed ID"
        elif self.option.choice == 1:
            return "crawl the summary based on id and corresponding database"
        elif self.option.choice == 2:
            return "crawl the pmc document based on given pmc id"
        elif self.option.choice == 6:
            return "pipeline"
        else:
            return "the woring mode is not correct."

    def start_crawl_based_on_choice(self):
        # 0=crawl pubmed id,1=crawl summary,2=crawl pmc doc,6=pipeline
        if self.option.choice == 0:
            self.logger.info("Start to search the pubmed id based on database and term")
            if self.option.term is "":
                self.logger.error("You should input term to search the pubmed id!")
                quit()
            else:
                print PubmedId(self.option).search_id_list(debug=True)
        elif self.option.choice == 1:
            self.logger.info("Start to search the documents' summary based on database and id")
            if self.option.pid is "":
                self.logger.error("You should input id to search the documents' summary!")
                quit()
            else:
                print PubmedSummary().get_summary("pubmed", self.option.pid)
        elif self.option.choice == 2:
            self.logger.info("Start to search the pmc documents based on database and id")
            if self.option.pid is "":
                self.logger.error("You should input the id of pmc to search the documents!")
                quit()
            else:
                print PubmedDoc().search_pmc(self.option.pid)
        elif self.option.choice == 6:
            self.logger.info("Start the pipeline of pubmed crawler")
            if self.option.processes < 0:
                self.sequential_pipeline()
            else:
                self.parallel_pipeline_thread()
        self.logger.info("Finish the crawler for pubmed. working mode: {w}" . format(w=self.get_work_mode()))

    def sequential_pipeline(self):
        self.logger.info("start pipeline. mode: sequential")
        summary, pmcdoc = pubdb.init_collection()

        self.logger.info("Start to get pubmed id.")
        pubmed_ids = sequentialPackage.get_pubmed_ids(self.option)
        pubmed_ids = sequentialPackage.get_npubmed_ids(pubmed_ids, summary)
        sequentialPackage.get_update_summary(pubmed_ids, summary, self.option.database)

        self.logger.info("Start to get pmc id.")
        pmc_ids = sequentialPackage.get_npmc_id(summary, pmcdoc)

        self.logger.info("Start to get pmc doc.")
        sequentialPackage.get_pmc_doc(pmc_ids, pmcdoc)

    def parallel_pipeline_thread(self):
        self.logger.info("start pipeline. mode: paralle through thread")
        summary, pmcdoc = pubdb.init_collection()
        self.logger.info("Start to get pubmed id.")
        pubmed_ids = sequentialPackage.get_pubmed_ids(self.option)
        pubmed_ids = sequentialPackage.get_npubmed_ids(pubmed_ids, summary)
        parallelPackage.get_update_summary_threads(self.option.processes, summary, pubmed_ids, self.option.database)

        self.logger.info("Start to get pmc id.")
        pmc_ids = sequentialPackage.get_npmc_id(summary, pmcdoc)
        self.logger.info("Start to get pmc doc.")
        parallelPackage.get_pmc_doc_threads(self.option.processes, pmcdoc, pmc_ids)
