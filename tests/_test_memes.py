#!/usr/bin/env python
# -*- coding: utf-8 -*-

from test_helpers import TestHelpers
helpers=TestHelpers()
helpers.add_relative_path()

# from lib.protomemes import get_protomeme_by_id,get_protomemes

from time import time
import numpy as np

from lib.vectorizer import get_protomemes_labels, get_global_similarities

from scipy.cluster.hierarchy import linkage, dendrogram, leaves_list

#
#
def get_similar_protomemes(_protomeme):

    get_similar_rows(0.7)

    if(sim < 0.8):
        print "Found similar"

def get_similar_rows(_threshold):
    
    similarity_matrix=get_global_similarities()

    similar_rows=[]
    for row in similarity_matrix:
        if(row[0] < threshold):
            similar_rows.append(row)
    return similar_rows

def get_similarities(p1,p2):
    
    matrix_data=[]

    # vectorize
    text_sim=get_text_sim(p1,p2)
    diffusion_sim=get_diff_sim(p1,p2)
    tweets_sim=get_tweets_sim(p1,p2)
    
    return matrix_data


path="/tmp"
similarity_matrix=get_global_similarities(path)
labels=get_protomemes_labels(path)

print " calculate matrix w average linkage algorithm"
linkage_matrix=linkage(similarity_matrix, method='average')
print " clusters: n_samples: %d, n_features: %d" % linkage_matrix.shape