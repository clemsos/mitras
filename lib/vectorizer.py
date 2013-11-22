#!/usr/bin/env python
# -*- coding: utf-8 -*-


from gensim import corpora, models, similarities
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer
import numpy as np

from time import time

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
    print " Create text corpus"
    corpus_text=[]
    for proto in _protomemes:
        # corpus_text.append(get_text_vector(proto))
        corpus_text.append(proto["value"]["txt"])
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