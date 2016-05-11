# -*- coding: utf-8 -*-
#
# Search documents summary based on the given 'database' and 'term',
# and return a list of pubmed id.
#
# Usage:
#   id = PubmedId(option)
#   id.search_id_list(debug=True)

import utils
import re
from logger import Logger
from urllib2 import urlopen
from bs4 import BeautifulSoup as BS
from settings.parameters import *

class PubmedId(object):
    def __init__(self, option):
        super(PubmedId, self).__init__()
        self.logger = Logger.get_logger(utils.get_fullname(self))
        self.logger.info("Search id list based on given `database` and `term`")
        self.baseURL = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        self.option = option

    def search_id_list(self, debug=False):
        query = self.baseURL + "esearch.fcgi?db={database}&term={term}&usehistory=y" . format(database=self.option.database, term=self.option.term)
        self.logger.info("search id based on 'database'={d} and 'term'={t}. searching url={url}" . format(d=self.option.database, t=self.option.term, url=query))
        content = str(BS(urlopen(query, timeout=TIMEOUT).read(), "lxml"))
        parsed_esearch = self.parse_esearchresult(content)
        self.logger.debug("get content:\n{d}" . format(d=content))
        self.logger.info("esearchresult (total): count={c}, querykey={q}, webenv={w}" . format(c=parsed_esearch["count"], q=parsed_esearch["querykey"], w=parsed_esearch["webenv"]))

        searched_result = []
        for retstart in xrange(0, parsed_esearch["count"], self.option.retmax):
            if debug is True and retstart > 10:
                break
            sub_query = self.baseURL + "esearch.fcgi?db={database}" . format(database=self.option.database)
            sub_query += "&query_key={q}&WebEnv={w}" .format(q=parsed_esearch["querykey"], w=parsed_esearch["webenv"])
            sub_query += "&retstart={start}&retmax={retmax}" . format(start=retstart, retmax=self.option.retmax)
            self.logger.debug("search id based on history{h}" . format(h=sub_query))
            tmp = str(BS(urlopen(sub_query, timeout=TIMEOUT).read(), "lxml"))
            searched_result += self.basic_parser(r"<id>(.*?)</id>", tmp)
        self.logger.info("esearchresult (recovered): count={c}, retmax={r}" . format(c=len(searched_result), r=self.option.retmax))
        return searched_result

    def parse_esearchresult(self, content):
        count = self.basic_parser(r"<esearchresult>.*?<count>(.*?)</count>.*?</esearchresult>", content)
        querykey = self.basic_parser(r"<esearchresult>.*?<querykey>(.*?)</querykey>.*?</esearchresult>", content)
        webenv = self.basic_parser(r"<esearchresult>.*?<webenv>(.*?)</webenv>.*?</esearchresult>", content)
        return {"count": int(count[0]), "querykey": querykey[0], "webenv": webenv[0]}

    def basic_parser(self, regex, content):
        pattern = re.compile(regex, re.S)
        return re.findall(pattern, content)

    def sub_id(self, iid):
        return re.filter(r"\D", '', iid)
