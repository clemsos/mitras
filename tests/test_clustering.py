#!/usr/bin/env python
# -*- coding: utf-8 -*-

from test_helpers import TestHelpers

helpers=TestHelpers()
helpers.add_relative_path()

from lib.protomemes import get_protomemes, build_corpus
import lib.vectorizer as vectorizer

import unittest
import numpy as np
# t00=time()
# print helpers.load_tweets("week1",1)
# class TestSequenceFunctions(unittest.TestCase):

count=2000
path="/tmp/tests"
pms=get_protomemes(None,count)
protomemes=np.array(pms) # convert to numpy array 

print "%d protomemes obtained." % len(protomemes)
print 

# for p in protomemes:
#     print p["value"]["users"]

vectorizer.compute_and_save_similarity_corpus(protomemes,path)

vectorizer.compute_cosine_similarities_from_corpus(path)
vectorizer.create_combined_similarities_index(path)