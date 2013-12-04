#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.protomemes import get_protomemes, create_txt_corpus_file,create_corpus_file
import lib.vectorizer as vectorizer
from lib.api import Similarity_API
import numpy as np


# path="/tmp/pms"
path="/home/clemsos/Dev/mitras/data/tmp"
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
count=707425 # should be the y dimension of the matrix
chunk_length=250 
api=Similarity_API(path,count,chunk_length)

# diff_corpus=corpora.MmCorpus(_path+"/diffusion.mm")
# count=len(diff_corpus)
# print " Starting linear combination for %d similarity measures"%count

# chunk size can be changed according to RAM 

api.create_combined_similarities_index()

# values= [(count,x) for x in range(0, len(api.types))]
# print values
# api.compute_similarities_using_multiple_processes(values)
# api.create_combined_similarities_index(path)