#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans , MiniBatchKMeans

from test_helpers import TestHelpers
from time import time

###############################################################################
# Get data

helpers=TestHelpers()
tweets=helpers.load_tweets("week1",100000)

number_clusters=10

###############################################################################
# Clean set
corpus=[]
STOP_TWEETS=["转发微博","轉發微博","分享图片"]

for t in list(tweets):
    # TODO : optimize remove most common tweets for ID-TDF
    # if t["txt"].encode('utf-8') not in STOP_TWEETS:
    dico=' '.join(x for x in t["dico"]) 
    # print dico
    corpus.append(dico)

print "%d tweets in corpus" % len(corpus)
# print "%d categories" % len(dataset.target_names)
print

###############################################################################
# Create TF-IDF set

print "Extracting features from the training dataset using a sparse vectorizer"
t0 = time()

tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)

# print type(tfidf_matrix)
print "done in %fs" % (time() - t0)
print "n_samples: %d, n_features: %d" % tfidf_matrix.shape
print


###############################################################################
# Compute with k-means

# km = MiniBatchKMeans(n_clusters=number_clusters, init='k-means++', n_init=1,init_size=1000,batch_size=1000, verbose=1)

# km = KMeans(n_clusters=number_clusters, init='random', max_iter=100, n_init=1, verbose=1)

# print "Clustering sparse data with %s" % km
# t0 = time()
# km.fit(tfidf_matrix)
# print "done in %0.3fs" % (time() - t0)