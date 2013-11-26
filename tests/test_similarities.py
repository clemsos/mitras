#!/usr/bin/env python
# -*- coding: utf-8 -*-

from test_helpers import TestHelpers
helpers=TestHelpers()
helpers.add_relative_path()

from lib.protomemes import get_protomeme_by_id,get_protomemes
import lib.vectorizer as vectorizer

count=100
path="/tmp/test"

protomemes=get_protomemes(None,count)
print "%d protomemes obtained." % len(protomemes)
print 

sim_matrix=vectorizer.create_global_similarity_matrix(protomemes,path)
print sim_matrix