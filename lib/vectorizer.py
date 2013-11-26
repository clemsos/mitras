#!/usr/bin/env python
# -*- coding: utf-8 -*-


from gensim import corpora, models, similarities, matutils
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from multiprocessing import Pool

import numpy as np
from time import time
import pickle
import os.path

# create index dictionary for all users
def create_dictionary(_corpus,_dic_path):
    print " Creating dictionary for diffusion."
    print ' Indexing...'
    t0 = time()

    dic_path=_dic_path

    # load if the file already exists

    dictionary = corpora.Dictionary(_corpus)
    dictionary.save(dic_path) # store the dictionary, for future reference
    print " dico saved at %s " % dic_path

    print " %d unique ids." % len(dictionary.token2id)
    print " done in %fs" % (time() - t0)
    print 
    return dictionary

# compute number of times each elements appears in the corpus
def create_frequency_vectors_corpus(_corpus,_dictionary,_corpus_path):
    print ' Computing frequency vectors'
    t0 = time()

    corpus_path=_corpus_path
    corpus = [_dictionary.doc2bow(t) for t in _corpus]
    corpora.MmCorpus.serialize(corpus_path, corpus) # store to disk, for later use
    print " dico saved at %s " % corpus_path

    print " %d records processed." % len(_corpus)
    print " done in %fs" % (time() - t0)
    print
    # pprint(corpus)
    # print corpus


# Utils
def create_and_store_labels_for_reference(_protomemes,_path):
    print "Storing protomemes labels and ids for future reference"
    labels=[]
    print ' WARNING : protomeme type should be defined during map-reduce'
    for p in _protomemes:
        
        # TODO : add type to map/reduce _id  during protomemes creation
        # mytype= p["_id"]["type"] 
        # name=p["_id"]["name"]
        
        name=p["_id"]

        try:
            mytype= p["value"]["type"]
        except KeyError:
            # TODO : remove dirty hack (add to map reduce)
            # print 'WARNING : --- type not defined'
            if p["_id"][0] == "h":
                mytype="urls"
            elif p["_id"][0] == "u":
                mytype="mentions"
            else :
                mytype="hashtags"


        labels.append((name, mytype))
    
    labels_path=_path+"/labels.txt"
    print " storing labels as file : %s"%labels_path
    outfile=open(labels_path,"wb")
    pickle.dump(labels, outfile)
    print


# TODO :
def compute_similarities_using_multiple_processes(l):
    '''process the test list elements in parallel'''
    
    print '  using multi-process pool'
    pool = Pool()
    results = pool.map(create_similarity_matrix, l)
    return results


# Gensim functions to create corpus
def has_corpus(_path,_type):
    corpus_path=_path+'/'+_type+'.mm'
    return os.path.exists(corpus_path)

def has_indexed_file(_path,_type):
    index_path=_path+'/'+_type+'.index'
    return os.path.exists(index_path)

def create_similarity_corpus(_corpus,_path, _type):

    print '-'*40
    print 'Vectorizing %s',_type
    print 

    # compute path
    my_path=_path+'/'+_type
    dic_path=my_path+'.dict'
    corpus_path=my_path+'.mm'

    if os.path.exists(corpus_path): 
        print " corpus and dict already exists %s, %s"(dict_path,corpus_path)
        pass
 
    elif os.path.exists(dic_path) :

        print ' loading existing dictionary from %s'% dic_path
        dictionary=corpora.Dictionary.load(dic_path)

    # if no dictionary exists, we have to compute dict and corpus
    else:

        # create index of values
        dictionary=create_dictionary(_corpus,dic_path)  

        # compute number of times in each corpus
        create_frequency_vectors_corpus(_corpus,dictionary,corpus_path)

def create_similarity_index(_corpus,_path):
    
    print " creating similarity index %s"%_corpus
    print " loading corpus from %s"%_path
    corpus=corpora.MmCorpus(_path+"/"+_corpus+".mm")
    print "",corpus

    index=similarities.MatrixSimilarity(corpus)
    
    # TODO : change class if more documents
    # index = similarities.Similarity(_path+'/tst', corpus, num_features=3173) # build the index
    file_path=_path+"/"+_corpus+".index"
    index.save(file_path)

    print " similarities saved as %s"%file_path
    print 
    # get similarities between the query and all index 
    # sims = index[corpus]

    # corpus_txt=matutils.MmReader(_path+"/text.mm")
    # corpus_twe=matutils.MmReader(_path+"/tweets.mm")

def text_corpus_to_tfidf(_path):
    print " computing TF-IDF"
    corpus=corpora.MmCorpus(_path+"/text.mm")
    tfidf = models.TfidfModel(corpus) 
    
    tfidf_corpus= tfidf[corpus]
    # print type(tfidf_corpus)
    # for doc in corpus_tfidf:
    #     print doc
    
    tfidf_path=_path+"/tfidf.mm"
    print " saving tfidf results at %s"%tfidf_path
    corpora.MmCorpus.serialize(tfidf_path, tfidf_corpus)
    print

# Public functions
def compute_and_save_similarity_corpus(_protomemes,_path): 
    
    if os.path.exists(_path+"/labels.txt"):
        print " labels already exist at %s/labels.txt"%_path
        pass
    else:
        # Store labels for future use
        create_and_store_labels_for_reference(_protomemes,_path)

    tstart=time()
    print 
    # STEP 1 
    print "Step 1 : Compute all vectors from %d protomemes"%len(_protomemes)
    print '#'*40
    print
    
    # TODO : use multi processing to improve computing
    # create corpus and dictionaries
    if not has_corpus(_path,"diffusion"):
        corpus=[]
        for p in _protomemes:
            corpus.append(p["value"]["diffusion"])

        create_similarity_corpus(corpus,_path,"diffusion")
    else:
        print " Diffusion vector corpus already exists %s"%(_path+"/diffusion.mm")
        print 
    if not has_corpus(_path,"tweets"):
        tweets_corpus=[]
        for p in _protomemes:
            tweets_corpus.append(p["value"]["tweets"])
        create_similarity_corpus(tweets_corpus,_path,"tweets")
    else:
        print " Tweets vector corpus already exists %s"%(_path+"/tweets.mm")
        print 
    if not has_corpus(_path,"text"):
        txt_corpus=[]
        for p in _protomemes:
            txt_corpus.append(p["value"]["txt"].encode("utf-8").split())
        create_similarity_corpus(txt_corpus,_path,"text")
    else:
        print " Text vector corpus already exists %s"%(_path+"/text.mm")
        print 
    if not has_corpus(_path,"users"):
        users_corpus=[]
        for p in _protomemes:
            users_corpus.append(p["value"]["users"])
        create_similarity_corpus(users_corpus,_path,"users")
    else:
        print " Users vector corpus already exists %s"%(_path+"/users.mm")
        print 
        
def compute_cosine_similarities_from_corpus(_path):

    print "Step 2 : Compute cosine similarities from corpus"
    print '#'*40
    print
    
    # modeling and transformation
    if not os.path.exists(_path+"/tfidf.mm"):
        text_corpus_to_tfidf(_path)
    else:
        print " TF-IDF corpus already processed : %s"%(_path+"/tfidf.index")
        print

    # user_to_frequency_vectors # user count    
    # tweets_to_binary_vectors # np.array are binary vectors already
    # diffusion_to_binary_vectors # np.array are binary vectors already

    # compute similarity
    if not has_indexed_file(_path,"users"):
        create_similarity_index("users",_path)
    else:
        print " Users already indexed : %s"%(_path+"/users.index")
        print

    if not has_indexed_file(_path,"diffusion"):
        create_similarity_index("diffusion",_path)
    else:
        print " Diffusion already indexed : %s"%(_path+"/diffusion.index")
        print

    if not has_indexed_file(_path,"tweets"):
        create_similarity_index("tweets",_path)
    else:
        print " Tweets already indexed : %s"%(_path+"/tweets.index")        
        print

    if not has_indexed_file(_path,"tfidf"):
        create_similarity_index("tfidf",_path)
    else:
        print " TF-IDF already indexed : %s"%(_path+"/tfidf.index")
        print

def create_combined_similarities_index(_path):

    # STEP 2
    print "Step 3 : Combine similarities index"
    print '#'*40
    print 

    t0=time()

    print ' loading similarity indexes'
    diff_index=similarities.MatrixSimilarity.load(_path+'/diffusion.index')
    twe_index=similarities.MatrixSimilarity.load(_path+'/tweets.index')
    txt_index=similarities.MatrixSimilarity.load(_path+'/tfidf.index')
    users_index=similarities.MatrixSimilarity.load(_path+'/users.index')

    print " loading corpora"
    diff_corpus=corpora.MmCorpus(_path+"/diffusion.mm")
    txt_corpus=corpora.MmCorpus(_path+"/text.mm")
    twe_corpus=corpora.MmCorpus(_path+"/tweets.mm")
    users_corpus=corpora.MmCorpus(_path+"/users.mm")

    diff=diff_index[diff_corpus]
    txt=txt_index[txt_corpus]
    tweets=twe_index[twe_corpus]
    users=users_index[users_corpus]


    print
    print " text similarity - n_samples: %d, n_features: %d "%diff.shape
    print " tweets similarity - n_samples: %d, n_features: %d "%tweets.shape
    print " diffusion similarity - n_samples: %d, n_features: %d "%txt.shape
    print " users similarity - n_samples: %d, n_features: %d "%users.shape

    print
    
    print " done in %fs"%(time()-t0)
    print


    print "Starting linear combination of similarity measures"

    # indices for linear combination optimization
    wt = 0.0
    wc = 0.7 
    wu = 0.1
    wd = 0.2
    
    if wt+wc+wu+wd != 1:
        raise ValueError("scale factors sum should equals 1")

    # TODO : add missing parameters
    print " weighting and scaling up matrix "
    combi=wc*txt +wd*diff +wt*tweets+wu*users
    print " values combination length :%d " % len(combi)

    # print(combi.shape)

    combi_path=_path+"/similarities_matrix.npy"
    combi_file=file(combi_path,"wb")
    print " storing similarity matrix as file : %s"%combi_path
    np.save(combi_file,combi)
    print 
    print "Similarities computation done ",
    print " in %fs"%(time()-t0)
    print 
    return combi


# api 
def get_protomemes_labels(_path):
    labels_path=_path+"/labels.txt"
    print " extracting labels from file : %s"%labels_path
    outfile=open(labels_path,"rb")
    labels=pickle.load(outfile)
    print
    return labels

def get_global_similarities(_path):
    matrix_binary_path=_path+"/similarities_matrix.npy"
    print ' loading similarities matrix from binary file %s'%matrix_binary_path
    sims=np.load(matrix_binary_path)
    return sims

