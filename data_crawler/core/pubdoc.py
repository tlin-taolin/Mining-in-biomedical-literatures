# -*- coding: utf-8 -*-
#
# Search documents summary based on the given 'database' and 'pubmed id',
# and return the summary corresponds to that id.
#
# Usage:
#   doc = PubmedDoc()
#   pmcdoc1 = doc.search_pmc("2684823")
#   pmcdoc2 = doc.search_pmc("212403")
#
#   title = doc.get_title(pmcdoc2)
#   authors = doc.get_authors(pmcdoc2)
#   authors = doc.get_authors(pmcdoc2)
#   abstract = doc.get_abstract(pmcdoc2)
#   parsed_doc = doc.parse_doc(pmcdoc2)
#   print parsed_doc["abstract"]
#   print parsed_doc["body"]
#   print parsed_doc["ref"]

import re
import utils
import os.path
import datetime
from logger import Logger
from urllib2 import urlopen, Request
from bs4 import BeautifulSoup as BS
from pyquery import PyQuery as pq
from settings.parameters import *


class PubmedDoc(object):
    """Get the pmc documents based on its id"""
    def __init__(self):
        super(PubmedDoc, self).__init__()
        self.logger = Logger.get_logger(utils.get_fullname(self))
        self.logger.info("Get the pmc documents based on its id")
        self.baseURL = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

    def check_local_pmc(self, pmc_file):
        return os.path.isfile(pmc_file)

    def get_pmc(self, query):
        pmc_file = DATABASE_POC + "PMC-" + pmc_id + "-.xml"
        if not self.check_local_pmc(pmc_file):
            to_store = urlopen(query, timeout=TIMEOUT).read()
            with open(pmc_file, "w") as to_xml:
                to_xml.write(to_store)
            return to_store
        else:
            with open(pmc_file, "r") as read_xml:
                return read_xml.read()

    def search_pmc(self, pmc_id):
        """fetch the documents' content (have pmc id)"""
        query = self.baseURL + "efetch.fcgi?db=pmc&id={id}" . format(id=pmc_id)
        self.logger.info("search the content of pmc document based on its 'id'={id}. searching url={url}" . format(id=pmc_id, url=query))
        try:
            content = BS(urlopen(query, timeout=TIMEOUT).read(), 'lxml')
        except:
            content = ""

        if "<?properties open_access?>" in content.encode('utf-8'):
            self.logger.info("access the open_access document. pmc_id={pid}" . format(pid=pmc_id))
            parsed_doc = self.eutils_parse_doc(content)
            return {
                "pmc_id": pmc_id,
                "abstract": parsed_doc[0],
                "body": parsed_doc[1],
                "entry_created_date": str(datetime.datetime.utcnow())
            }
        else:
            return ""
            self.logger.info("cannot access the document (pmc_id={pid}). Crawl it by web crawler!" . format(pid=pmc_id))
            parsed_doc = self.advanced_parse_doc(pmc_id)
            return {
                "pmc_id": pmc_id,
                "abstract": parsed_doc[0],
                "keyword": parsed_doc[1],
                "body": parsed_doc[2],
                "bib": parsed_doc[3],
                "entry_created_date": str(datetime.datetime.utcnow())
            }

    def eutils_parse_doc(self, content):
        abstract = [a.get_text() for a in content.findAll("abstract")]
        raw_body = [b for b in content.findAll("body")]
        body = []
        for b in raw_body:
            body += [x.get_text() for x in b.findAll("sec")]
        return abstract, body

    def advanced_parse_doc(self, pmc_id):
        url = "http://www.ncbi.nlm.nih.gov/pmc/articles/PMC" + pmc_id
        self.logger.info("crawl the web: {w}" . format(w=url))
        headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
        request = Request(url, None, headers)

        try:
            response = urlopen(request, timeout=TIMEOUT)
            data = response.read()
            response.close()

            bs_data = BS(data, 'lxml')
            doc = bs_data.findAll("div", {"class": "tsec sec"})
            raw_abstract = doc[0]
            raw_body = doc[1: -1]
            raw_bib = doc[-1]

            abstract = [p.get_text() for p in raw_abstract.findAll('p')]
            keyword = [k.get_text() for k in raw_abstract.findAll("span", {"class", 'kwd-text'})]

            body = []
            for sec in raw_body:
                body += [p.get_text() for p in sec.findAll('p')]

            bib = [c.get_text() for c in raw_bib.findAll("span", {"class": "element-citation"})]
            return abstract, keyword, body, bib
        except Exception:
            self.logger.warning("Failed to crawl the link due the error from the web")
            return None, None, None, None
