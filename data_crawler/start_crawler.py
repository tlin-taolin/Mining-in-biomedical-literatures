# -*- coding: utf-8 -*-
#
#

from core import *
from settings import *
from optparse import OptionParser


def main(option):
    logger = Logger.get_logger('Crawler')
    logger.info("START THE CRAWLER!")

    pubmed = PubMed(option)

    pubmed.start_crawl_based_on_choice()

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-d", 	"--db", 			dest="database", 		default="pubmed", 		type="string", 				help="the database to search")
    parser.add_option("-t", 	"--term", 			dest="term", 			default="", 			type="string", 				help="Entrez text query. All special characters must be URL encoded.")
    parser.add_option("-i", 	"--pid", 			dest="pid", 			default="", 			type="string", 				help="single pid/ a comma-delimited (by `,`) list of pids.")
    parser.add_option("-a", 	"--retmax", 		dest="retmax", 			default=200, 			type="int", 				help="number of UIDs returned in the XML; default=20")
    parser.add_option("-m", 	"--retmode", 		dest="retmode", 		default="", 			type="string", 				help="determines the format of the returned output")
    parser.add_option("-e", 	"--rettype", 		dest="rettype", 		default="", 			type="string", 				help="the parameter specifies the record view returned")
    parser.add_option("-p", 	"--processes", 		dest="processes", 		default=-1, 			type="int", 				help="number of process used in parallel (default=-1...all)")
    parser.add_option("-c", 	"--choice", 		dest="choice", 			default=6, 			    type="int", 		        help="the choice of the crawl, default=6. 0=crawl pubmed id,1=crawl summary,2=crawl pmc doc,6=pipeline (advanced usage.)")
    parser.add_option("-o", 	"--output", 		dest="output", 			default=False, 			action="store_true", 		help="output the crawler results")
    parser.add_option("-u", 	"--outputpath", 	dest="outputpath", 		default="", 			type="string", 				help="the path that used for output the result of crawler")

    (option, args) = parser.parse_args()

    out = main(option)

    if option.output:
        print("output the crawled data to the current...")
        print("done!")
