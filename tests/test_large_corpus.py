#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from gensim import corpora, models, similarities

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

dic_path = '/tmp/test/diffusion.dict'
# corpus_path = '/tmp/test/diffusion.mm'
# corpus_path = '/tmp/test/diffusion.mm'

dictionary=corpora.Dictionary.load(dic_path)

class MyCorpus(object):
    def __iter__(self):
        for line in open(corpus_path):
            # assume there's one document per line, tokens separated by whitespace
            yield dictionary.doc2bow(line.lower().split())




corpus_memory_friendly = MyCorpus()

print corpus_memory_friendly

for vector in corpus_memory_friendly:
    print vector