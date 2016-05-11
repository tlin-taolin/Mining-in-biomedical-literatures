# -*- coding: utf-8 -*-
#
# Search documents summary based on the given 'database' and 'pubmed id',
# and return the summary corresponds to that id.
#
# Usage:
#   summary = PubmedSummary()
#   summary_dict = summary.get_summary(option.database, "212403")
#   print summary_dict["author"], summary_dict["pub_date"]
#   print summary_dict["jounal_name"], summary_dict["jounal_full_name"]
#   print summary_dict["pmc_id"]

import re
import utils
import datetime
from logger import Logger
from urllib2 import urlopen
from bs4 import BeautifulSoup as BS
from pyquery import PyQuery as pq
from settings.parameters import *


class PubmedSummary(object):
    """Search documents summary based on the given `database` and `pid`"""
    def __init__(self):
        super(PubmedSummary, self).__init__()
        self.logger = Logger.get_logger(utils.get_fullname(self))
        self.logger.info("Search documents' summary based on given 'database' and 'id'")
        self.baseURL = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

    def search_summary(self, db, pid):
        query = self.baseURL + "esummary.fcgi?db={database}&id={id}&rettype=abstract&retmode=text" . format(database=db, id=pid)
        self.logger.info("search documents' summary based on 'database'={d} and 'id'={id}. searching url={url}" . format(d=db, id=pid, url=query))
        try:
            return pq(str(BS(urlopen(query, timeout=TIMEOUT).read(), "lxml")))
        except:
            return ""

    def get_summary(self, db, pid):
        content = self.search_summary(db, pid)
        try:
            summary = {
                "authors": self.get_authors(content),
                "pub_date": self.get_pub_date(content),
                "journal_name": self.get_journal_name(content),
                "journal_full_name": self.get_journal_full_name(content),
                "pmc_id": self.get_id_pmc(content),
                "title": self.get_title(content),
                "pubmed_id": self.get_id_pubmed(content),
                "entry_created_date": str(datetime.datetime.utcnow())
            }
        except:
            summary = ""
        return summary

    def get_attr(self, content, attr):
        return content('[name="%s"]' % attr)

    def get_authors(self, content):
        return [author_label.text for author_label in self.get_attr(content, 'Author')]

    def get_title(self, content):
        return self.get_attr(content, 'Title').text()

    def get_pub_date(self, content):
        return self.get_attr(content, 'PubDate').text()

    def get_journal_name(self, content):
        return self.get_attr(content, 'Source').text()

    def get_journal_full_name(self, content):
        return self.get_attr(content, 'FullJournalName').text()

    def get_id_pmc(self, content):
        id = self.get_attr(content, 'pmc').text()
        return re.sub(r'\D', '', id)

    def get_id_pubmed(self, content):
        try:
            for l in self.get_attr(content, 'pubmed').items():
                id = l.text()
                break
        except:
            id = ""
        if id is "":
            id = self.get_attr(content, 'pmid').text()
        return re.sub(r'\D', '', id)
