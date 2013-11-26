#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.protomemes import get_protomemes, create_txt_corpus_file,create_corpus_file
import lib.vectorizer as vectorizer
import numpy as np

# from lib.mongo import MongoDB

# db=MongoDB("weibodata").db
# count=db["protomemes"].count()
# print str(count)+" tweets in the db"

# count=1000
path="/tmp/week1"
# pms=get_protomemes(None,0)
# protomemes=np.array([pms) # convert to numpy array 

# print "%d protomemes obtained." % len(protomemes)
# print 
# filename=path+"/protomemes.txt"
# f=open(filename, 'rb')
# print len(list(f))
# for i,l in enumerate(list(f)):
#     print i

# compute corpus

types=["txt","diffusion","tweets","users"]

for t in types:
    create_corpus_file(t,0,path)

# compute matrix from corpus
vectorizer.compute_and_save_similarity_corpus(path)

# # transform to similarities
# vectorizer.compute_cosine_similarities_from_corpus(path)

# # combine similarities
# vectorizer.create_combined_similarities_index(path)