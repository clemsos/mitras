#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.protomemes import get_protomemes, create_txt_corpus_file,create_corpus_file
import lib.vectorizer as vectorizer
import numpy as np


path="/tmp/pms"
types=["txt","diffusion","tweets","users"]

# compute corpus
for t in types:
    create_corpus_file(t,0,path)

# corpus=corpora.MmCorpus(path+"/text.mm")
# print corpus

# compute matrix from corpus
vectorizer.compute_and_save_similarity_corpus(path)

# # transform to similarities
vectorizer.compute_cosine_similarities_from_corpus(path)

# # combine similarities
vectorizer.create_combined_similarities_index(path)