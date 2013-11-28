#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

This script just show the basic workflow to compute TF-IDF similarity matrix with Gensim 


OUTPUT :

clemsos@miner $ python gensim_workflow.py 


How to use Gensim to compute TF-IDF similarity step by step
----------
Let's start with a raw corpus :<type 'list'>

STEP 1 : Index and vectorize
----------
We create a dictionary, an index of all unique values: <class 'gensim.corpora.dictionary.Dictionary'>
Then convert convert tokenized documents to vectors: <type 'list'>
Save the vectorized corpus as a .mm file

STEP 2 : Transform and compute similarity between corpuses
----------
We load our dictionary : <class 'gensim.corpora.dictionary.Dictionary'>
We load our vector corpus : <class 'gensim.corpora.mmcorpus.MmCorpus'> 
We initialize our TF-IDF transformation tool : <class 'gensim.models.tfidfmodel.TfidfModel'>
We convert our vectors corpus to TF-IDF space : <class 'gensim.interfaces.TransformedCorpus'>

STEP 3 : Create similarity matrix of all files
----------
We compute similarities from the TF-IDF corpus : <class 'gensim.similarities.docsim.MatrixSimilarity'>
We get a similarity matrix for all documents in the corpus <type 'numpy.ndarray'>

Done in 0.011s

'''
from gensim import corpora, models, similarities
from time import time

t0=time()

# keywords have been extracted and stopwords removed.

tweets=[[   "uKPK5TSP1",    "uWYNOWTTW",    "uW0EHDVVF",    "u1CR2YCSJ",    "uMLLWIWH2",    "uLCMN3QX0",    "uJ2O35J0D",    "uWWBY3JBU",    "uKPK5TSP1",    "uWYNOWTTW",    "uW0EHDVVF",    "u1CR2YCSJ",    "uMLLWIWH2" ],
 [  "uHRVJ1ZI3" ],
 [  "uQSMQTET1",  "uQSMQTET1" ],
 [],
 [  "uVEQL3R0D",  "uB4HFM1W5",  "uUPW4F1M1",  "uWWBOTCJT",  "uWWBOTCJT" ] ,
 [  "uNEGOAOAK" ],
  [    "u1CR2YCSJ",    "uMLLWIWH2",    "uLCMN3QX0",    "uJ2O35J0D",    "uWWBY3JBU",    "uKPK5TSP1",    "uWYNOWTTW",    "uW0EHDVVF",    "u1CR2YCSJ",    "uMLLWIWH2" ]] 

print "How to use Gensim to compute TF-IDF similarity step by step"
print '-'*10
print "Let's start with a raw corpus :%s"%type(tweets)
print
# STEP 1 : Compile corpus and dictionary
print "STEP 1 : Index and vectorize"
print '-'*10

# create dictionary (index of each element)
dictionary = corpora.Dictionary(tweets)
dictionary.save('/tmp/tweets.dict') # store the dictionary, for future reference
print "We create a dictionary, an index of all unique values: %s"%type(dictionary)

# compile corpus (vectors number of times each elements appears)
raw_corpus = [dictionary.doc2bow(t) for t in tweets]
print "Then convert convert tokenized documents to vectors: %s"% type(raw_corpus)
corpora.MmCorpus.serialize('/tmp/tweets.mm', raw_corpus) # store to disk
print "Save the vectorized corpus as a .mm file"
print

# STEP 2 : similarity between corpuses
print "STEP 2 : Transform and compute similarity between corpuses"
print '-'*10
dictionary = corpora.Dictionary.load('/tmp/tweets.dict')
print "We load our dictionary : %s"% type(dictionary)

corpus = corpora.MmCorpus('/tmp/tweets.mm')
print "We load our vector corpus : %s "% type(corpus) 

# Transform Text with TF-IDF
# tfidf = models.TfidfModel(corpus) # step 1 -- initialize a model
# print "We initialize our TF-IDF transformation tool : %s"%type(tfidf)

# # corpus tf-idf
# corpus_tfidf = tfidf[corpus]
# print "We convert our vectors corpus to TF-IDF space : %s"%type(corpus_tfidf)
# print

# STEP 3 : Create similarity matrix of all files
print "STEP 3 : Create similarity matrix of all files"
print '-'*10
index = similarities.MatrixSimilarity(corpus)
print "We compute similarities from the TF-IDF corpus : %s"%type(index)
index.save('/tmp/deerwester.index')
index = similarities.MatrixSimilarity.load('/tmp/deerwester.index')

sims = index[corpus]
print "We get a similarity matrix for all documents in the corpus %s"% type(sims)
print 
print "Done in %.3fs"%(time()-t0)

print sims
# print list(enumerate(sims))
# sims = sorted(enumerate(sims), key=lambda item: item[1])
# print sims # print sorted (document number, similarity score) 2-tuples