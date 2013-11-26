#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.protomemes import get_protomemes
import lib.vectorizer as vectorizer
import numpy as np

from lib.mongo import MongoDB

db=MongoDB("weibodata").db
count=db["protomemes"].count()
# print str(count)+" tweets in the db"

# count=1000
path="/tmp/week1"
pms=get_protomemes(None,count)
protomemes=np.array([pms]) # convert to numpy array 

print "%d protomemes obtained." % len(protomemes)
# print 

# for p in protomemes:
#     print p["value"]["users"]

# compute matrix from corpus
vectorizer.compute_and_save_similarity_corpus(protomemes,path)

# transform to similarities
vectorizer.compute_cosine_similarities_from_corpus(path)

# combine similarities
vectorizer.create_combined_similarities_index(path)