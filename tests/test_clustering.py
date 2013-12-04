#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import numpy as np

from test_helpers import TestHelpers

helpers=TestHelpers()
helpers.add_relative_path()

from lib.api import Similarity_API
from lib.clusters import get_linkage_matrix
from time import time

# from scipy.cluster.hierarchy import linkage, dendrogram, leaves_list
import fastcluster 

t0=time()
path="/home/clemsos/Dev/mitras/data/tmp"
chunk_size=2500 # cut the whole dataset into chunks so it can be processed
protomemes_count= 43959#db["hashtags"].count()

api=Similarity_API(path,protomemes_count,chunk_size)
print 

sims=api.get_similarity_matrix()
print sims.shape

similarity_treshold = 0.7 # minimum value of similarity between protomemes
similar_protomemes_treshold=20
print 'getting rows with %d protomemes that are at least %.3fx similar'%(similar_protomemes_treshold,similarity_treshold)

# get row numbers
remarquable_rows=np.where((sims > similarity_treshold).sum(axis=1) >= similar_protomemes_treshold)[0]

# print type(remarquable_rows)
print "%d memes found"%len(remarquable_rows)
print remarquable_rows


# get memes data 

print " done in %.3fs"%(time()-t0)
print



print 
print " done in %.3fs"%(time()-t0)