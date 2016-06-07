# -*- coding: utf-8 -*-
#


class PhenotypeInfo(object):
    def __init__(self, line):
        self.id = str(line[0])
        self.phenotype = line[1]
        self.shown_pheno = line[2]
        self.category = line[3]
