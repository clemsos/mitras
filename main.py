#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.mongo import MongoDB
from lib.protomemes import get_protomemes
from lib.vectorizer import vectorize_text, tdidf, create_dictionary,get_frequency_vectors,create_matrix_from_vectors, cosine_similarity

import numpy as np
from time import time
import pylab
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.cluster.vq import kmeans,vq
from scipy.spatial.distance import pdist, squareform
from matplotlib import pyplot


# Variables
collection="week1"

# Connect to Mongo
db=MongoDB("weibodata").db
count = db[collection].count()
# count= 0 #data.count()

protomemes=get_protomemes("hashtags", count ,collection)

print "%d protomemes obtained." % len(protomemes)
print 

print '#'*40
print "Step 1 : Compute all vectors from protomemes"

##################################################################
# Text similarity (TF-IDF)
#

print '-'*40
print "Vectorizing tweets text"
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
    diffusion.append(proto["diffusion"])
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
    binary_tweets.append(proto["tweets"])

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
print "Compute cosine similarities from corpus"

t0=time()

text_sim=[cosine_similarity(pm, text_matrix)[0] for pm in text_matrix]
diffusion_sim=[cosine_similarity(pm, diffusion_matrix)[0] for pm in diffusion_matrix]
tweets_sim= [cosine_similarity(pm, tweets_matrix) for pm in tweets_matrix]

print " done in %fs" % (time() - t0)

print 
# linear combination of similarity measures,
print "Starting linear combination of similarity measures,"
wt = 0.0
wc = 0.7 
wu = 0.1
wd = 0.2

if wt+wc+wu+wd != 1:
    # TODO : throw error here
    print "ERROR : scale factors sum should equals 1"

# TODO : add missing parameters
print " weighting and scaling up matrix "
combi=wc*np.array(text_sim) +wd*np.array(diffusion_sim) #+wt*np.array(tweets_sim)

print " computing clusters with average linkage algorithm"
clusters=linkage(combi, method='average')
print " Cluters: n_samples: %d, n_features: %d" % clusters.shape

print " plotting data and generating images"
#use vq() to get as assignment for each obs.
assignment,cdist = vq(clusters,clusters)
pyplot.scatter(clusters[:,0], clusters[:,1], c=assignment)
pyplot.show()