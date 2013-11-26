#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import lib.vectorizer as vectorizer
import lib.clusters as clusters

path="/tmp"

sims=vectorizer.get_global_similarities(path)
print sims

labels=vectorizer.get_protomemes_labels(path)

linkage_matrix=clusters.get_linkage_matrix(sims)
clusters.explain_linkage_clusters(linkage_matrix,labels)