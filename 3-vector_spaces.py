#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter
from lib.mongo import MongoDB
# from models.protomeme import Protomeme
from gensim import corpora, models, similarities
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

import pylab
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.cluster.vq import kmeans,vq
from scipy.spatial.distance import pdist, squareform
from matplotlib import pyplot

from time import time
from pprint import pprint

# Variables
collection="week1"  

# Connect to Mongo
db=MongoDB("protomemes").db
data=db[collection]
protomemes_count= 100 #data.count()
print 10*"-"
print
print "%d required to the db" % protomemes_count

# compile all keywords from tweets
def get_text_vector(protomeme):
    # print len(protomeme["txt"])
    txt_vector=""
    for t in protomeme["txt"]:
        txt_vector+=' '.join(x for x in t) 
    # print txt_vector
    return txt_vector

# concanate text as a vector
def vectorize_text(_protomemes):
    print " Computing text vectors from protomemes"

    corpus_text=[]
    for proto in _protomemes:
        corpus_text.append(get_text_vector(proto))
    return corpus_text

# compute term frequency / inverse term frequency
def tdidf(corpus_text):
    print " Extracting features from the text corpus using a sparse vectorizer (TF-IDF)"
    t0 = time()

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(corpus_text)

    # print type(tfidf_matrix)
    print " done in %fs" % (time() - t0)
    print " Matrix : n_samples: %d, n_features: %d" % tfidf_matrix.shape
    print
    return tfidf_matrix.toarray()

# remove records that appear only once in the corpus
def remove_singleton_from_corpus(_corpus):
    print 'remove singleton from cropus'
    all_tokens = sum(_corpus, [])
    tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
    corpus_ok = [[word for word in text if word not in tokens_once] for text in _corpus]
    return corpus_ok

# create index dictionary for all users
def create_dictionary(_corpus):
    print ' Indexing...'
    t0 = time()
    # TODO : save file name
    dic_path='/tmp/weibo.dict'
    dictionary = corpora.Dictionary(_corpus)
    dictionary.save(dic_path) # store the dictionary, for future reference
    print " %d unique ids." % len(dictionary.token2id)
    print " done in %fs" % (time() - t0)
    print " dico saved at %s " % dic_path
    print 
    return dictionary

# compute number of times each users is in each protomeme as vectors
def get_frequency_vectors(_corpus,_dictionary):
    print ' Computing frequency vectors'
    t0 = time()
    corpus_path='/tmp/weibo.mm'
    corpus = [_dictionary.doc2bow(t) for t in _corpus]
    corpora.MmCorpus.serialize(corpus_path, corpus) # store to disk, for later use
    print " %d records processed." % len(_corpus)
    print " done in %fs" % (time() - t0)
    print " dico saved at %s " % corpus_path
    print
    # pprint(corpus)
    return corpus

# create clean sklearn numpy matrix
def create_matrix_from_vectors(_vector_corpus):
    print ' Creating matrix (numpy+sklearn)'
    t0 = time()
    vec = DictVectorizer()
    # format properly
    # TODO : optimize this
    final=[]
    for c in _vector_corpus:
        h={}
        # print c
        for hh in c:
            h[hh[0]]=hh[1]
        final.append(h)
    
    # create matrix 
    matrix=vec.fit_transform(final).toarray()

    print " Matrix size : n_samples: %d, n_features: %d" % matrix.shape
    print " done in %fs" % (time() - t0)
    print 
    # print matrix
    # print vec.get_feature_names()
    return matrix

query={}
protomemes= list(data.find(query).limit(protomemes_count))

print "%d protomemes obtained." % len(protomemes)
print "Processing data..."
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

diffusion=[]
for proto in protomemes:
    diffusion.append(proto["users"])

dictionary=create_dictionary(diffusion)
vector_diffusion_corpus=get_frequency_vectors(diffusion,dictionary)
diffusion_matrix=create_matrix_from_vectors(vector_diffusion_corpus)


##################################################################
# Binary tweets
#

print '-'*40
print "Vectorizing tweets ids"
print

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
print '-'*40
print "TODO : Tweet simple similarity "
print 


##################################################################
# STEP 2 
# Compute similarities
#

# sims={}

print '#'*40
print
print "Step 2 : Compute cosine similarities based on corpus"
print " text_matrix - n_samples: %d, n_features: %d "%text_matrix.shape
print " tweets_matrix - n_samples: %d, n_features: %d "%tweets_matrix.shape
print " diffusion_matrix - n_samples: %d, n_features: %d "%diffusion_matrix.shape
print

text_sim=[cosine_similarity(pm, text_matrix)[0] for pm in text_matrix]
diffusion_sim=[cosine_similarity(pm, diffusion_matrix)[0] for pm in diffusion_matrix]
tweets_sim= [cosine_similarity(pm, tweets_matrix) for pm in tweets_matrix]

# BUG : tweet_sim not working
# print tweets_sim 

for p in diffusion_sim:
    print p
# print len(text_sim)
##################################################################
# STEP 3
# Combine and plot similarities
#

# TODO : add error if matrix size is different
print '#'*40
print "Step 3 : Combine similarities from the corpus"
print 
print "All records should be equal size"
print "text_sim",len(text_sim)
print "diffusion_sim",len(diffusion_sim)
print "tweets_sim",len(tweets_sim)
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

# TODO add missing parameters
# print np.array(text_sim).shape
# print np.array(diffusion_sim).shape
combi=wc*np.array(text_sim) +wd*np.array(diffusion_sim)
# print combi.shape
# combi=wt*text_sim +wc*tweets_sim +wd*diffusion_sim #+wu*users_matrix

# print combi
# Compute clusters
# TODO : change method to "average"
clusters=linkage(combi, method='average')
print clusters.shape

#use vq() to get as assignment for each obs.
assignment,cdist = vq(clusters,clusters)
pyplot.scatter(clusters[:,0], clusters[:,1], c=assignment)
pyplot.show()