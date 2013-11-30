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

t0=time()
path="/home/clemsos/Dev/mitras/data/tmp"
count =707425
chunk_length=250

api=Similarity_API(path,count,chunk_length)

data=api.get_chunk(260)

print " loaded in %.3fs"%(time()-t0)
print
t1=time()
get_linkage_matrix(data)
print " computed in %.3fs"%(time()-t1)
print 
print " done in %.3fs"%(time()-t0)