#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.mongo import MongoDB
from lib.protomemes import get_protomemes
from lib.vectorizer import vectorize_text, tdidf, create_dictionary,get_frequency_vectors,create_matrix_from_vectors
from sklearn.metrics.pairwise import cosine_similarity
from lib.plot import augmented_dendrogram

from time import time
from multiprocessing import Pool

import numpy as np

from scipy import array as sparray
from scipy.cluster.hierarchy import linkage, dendrogram, leaves_list
from scipy.cluster.vq import kmeans,vq
from scipy.spatial.distance import pdist, squareform

import pylab
import matplotlib.pyplot as plt

# Variables
# collection="week1"
# Connect to Mongo
# db=MongoDB("weibodata").db
# count = db[collection].count()

t00=time()

count=100
pms=get_protomemes(None,count)
# convert to numpy array 
protomemes=np.array(pms)

print "%d protomemes obtained." % len(protomemes)
print 

print
print "Label matrix with protomemes description"

try:
    labels=[ p["value"]["type"] +" : "+p["_id"] for p in protomemes ]
except KeyError:
    labels=[]


print " length of labels %d"%len(labels)

print '#'*40
print "Step 1 : Compute all vectors from protomemes"

##################################################################
# Text similarity (TF-IDF)
#

print '-'*40
print "Computing text vectors from protomemes"
print 

corpus=vectorize_text(protomemes)
text_matrix=tdidf(corpus)

##################################################################
# Diffusion similarity
# 

print '-'*40
print 'Vectorizing diffusion using RT/mentions users list'
print 

print " Creating dictionary for diffusion"
diffusion=[]
for proto in protomemes:
    diffusion.append(proto["value"]["diffusion"])
dictionary=create_dictionary(diffusion)

vector_diffusion_corpus=get_frequency_vectors(diffusion,dictionary)
diffusion_matrix=create_matrix_from_vectors(vector_diffusion_corpus)

##################################################################
# Binary tweets
#

print '-'*40
print "Vectorizing tweets ids"
print

print " Creating dictionary for binary tweets"
binary_tweets=[]
for proto in protomemes:
    binary_tweets.append(proto["value"]["tweets"])

tweet_dic=create_dictionary(binary_tweets)
tweet_corpus=get_frequency_vectors(binary_tweets,tweet_dic)
tweets_matrix=create_matrix_from_vectors(tweet_corpus)

##################################################################
# User similarity
# TODO : add all ids of user to protomemes (should be mined in prepare.py)
#
# print '-'*40
# print "TODO : Tweet simple similarity "
# print 

##################################################################
# STEP 2 
# Compute similarities
#

print "Step 2 : Compare and combine matrix to detect clusters"
print '#'*40
print
print " text_matrix - n_samples: %d, n_features: %d "%text_matrix.shape
print " tweets_matrix - n_samples: %d, n_features: %d "%tweets_matrix.shape
print " diffusion_matrix - n_samples: %d, n_features: %d "%diffusion_matrix.shape
print
print " Compute cosine similarities from corpus"

def compute_cosine(matrix):
    """Worker function for multiprocessing"""

    print '  worker : computation process started'
    t1=time()
    cos=[cosine_similarity(matrix, pm)[0] for pm in matrix]
    # sleep(2)
    print " Cosine computed in",
    print " in %fs"%(time()-t1)
    return cos

def compute_similarities_using_multiple_processes(l):
    '''process the test list elements in parallel'''
    
    print ' creating multi-process pool'
    pool = Pool()
    results = pool.map(compute_cosine, l)
    return results


t0=time()

# multi processing to improve computing
results=compute_cosine_using_multiple_processes([text_matrix,diffusion_matrix,tweets_matrix])

print "  done in %fs" % (time() - t0)

text_sim=results[0]
diffusion_sim=results[1]
tweets_sim=results[2]

# TODO : fallback on single-threaded computing if CPU doesn't support multiprocessing
# text_sim=[cosine_similarity(pm, text_matrix)[0] for pm in text_matrix]
# diffusion_sim=[cosine_similarity(pm, diffusion_matrix)[0] for pm in diffusion_matrix]
# tweets_sim= [cosine_similarity(pm, tweets_matrix) for pm in tweets_matrix]

print 
# linear combination of similarity measures,
print "Starting linear combination of similarity measures,"
wt = 0.0
wc = 0.7 
wu = 0.1
wd = 0.2

if wt+wc+wu+wd != 1:
    raise ValueError("scale factors sum should equals 1")

# TODO : add missing parameters
print " weighting and scaling up matrix "
combi=wc*np.array(text_sim) +wd*np.array(diffusion_sim) +wt*np.array(tweets_sim)
print " combination length :%d " % len(combi)

print " calculate matrix w average linkage algorithm"
linkage_matrix=linkage(combi, method='average')
print " clusters: n_samples: %d, n_features: %d" % linkage_matrix.shape


# get order from dendrogram leaves
reordered = leaves_list(linkage_matrix)

# reorder the data matrix and row headers according to leaves
ordered_data_matrix = combi[reordered,:]

# do the same for the row headers
row_headers = np.array(labels)
ordered_row_headers = row_headers[reordered,:]

print
print " plotting data and generating images"

# use vq() to get as assignment for each obs.
# assignment,cdist = vq(clusters,clusters)
# plt.scatter(clusters[:,0], clusters[:,1], c=assignment)
# plt.show()
# plt.clf()


show_leaf_counts = False
ddata = augmented_dendrogram(linkage_matrix,
               color_threshold=1,
               p=60,
               truncate_mode='lastp',
               show_leaf_counts=show_leaf_counts,
               )

plt.title("Dendogram for %s protomemes"%len(protomemes))

plt.show()

print " everything done in %fs" % (time() - t00)