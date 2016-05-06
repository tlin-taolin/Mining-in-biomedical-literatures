# -*- coding: utf-8 -*-
#
# a parallel worker
#

import random
import time
from Queue import Queue
from threading import Thread
from settings.parameters import *
from pubsummary import PubmedSummary
from pubdoc import PubmedDoc


def random_sleep():
    return random.uniform(0, DOWNLOAD_DELAY)


class PMCIdThread(Thread):
    def __init__(self, queue, summary, db):
        Thread.__init__(self)
        self.queue = queue
        self.ps = PubmedSummary()
        self.summary = summary
        self.db = db

    def run(self):
        while True:
            pid = self.queue.get()
            tmp = self.ps.get_summary(self.db, pid)
            time.sleep(random_sleep())
            self.queue.task_done()
            try:
                self.summary.insert_one(tmp)
            except:
                pass


def get_update_summary_threads(num_of_thread, summary, pubmed_ids, db):
    queue = Queue()
    # Create num_of_thread worker-threads
    for x in range(num_of_thread):
        worker = PMCIdThread(queue, summary, db)
        # Setting daemon to True will let the main thread exit even though
        # the workers are blocking.
        worker.daemon = True
        worker.start()
    # Put the tasks into the queue as a tuple
    for pubmed_id in pubmed_ids:
        queue.put(pubmed_id)
    queue.join()


class PMCdocThread(Thread):
    def __init__(self, queue, pmcdoc):
        Thread.__init__(self)
        self.queue = queue
        self.doc = PubmedDoc()
        self.pmcdoc = pmcdoc

    def run(self):
        while True:
            pmc_id = self.queue.get()
            tmp = self.doc.search_pmc(pmc_id)
            time.sleep(random_sleep())
            self.queue.task_done()
            if tmp is not None:
                try:
                    self.pmcdoc.insert_one(tmp)
                except:
                    pass


def get_pmc_doc_threads(num_of_thread, pmcdoc, pmc_ids):
    queue = Queue()
    # Create num_of_thread worker-threads
    for x in range(num_of_thread):
        worker = PMCdocThread(queue, pmcdoc)
        # Setting daemon to True will let the main thread exit even though
        # the workers are blocking.
        worker.daemon = True
        worker.start()
    # Put the tasks into the queue as a tuple
    for pmc_id in pmc_ids:
        queue.put(pmc_id)
    queue.join()
