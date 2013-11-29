#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
# import lib.vectorizer as vectorizer
from lib.protomemes import create_labels_file
import lib.clusters as clusters
from lib.api import Protomemes_API

path="/home/clemsos/Dev/mitras/data/tmp"

# TODO : 
# create_labels_file(path)

# api=Protomemes_API()
# labels=api.get_labels()

# sims=vectorizer.get_global_similarities(path)
# print sims
# linkage_matrix=clusters.get_linkage_matrix(sims)
# clusters.explain_linkage_clusters(linkage_matrix,labels)