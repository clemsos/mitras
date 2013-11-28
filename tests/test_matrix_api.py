#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gensim import corpora, models, similarities, matutils, interfaces
import numpy as np
from test_helpers import TestHelpers

helpers=TestHelpers()
helpers.add_relative_path()

from lib.api import Similarity_API

path="/home/clemsos/Dev/mitras/data/tmp"

api=Similarity_API(path)

print "Starting linear combination of similarity measures"
print api.get_a_row(10)
print api.get_a_row(11)
print api.get_a_row(12)
print api.get_a_row(201322)
print api.get_a_row(222)