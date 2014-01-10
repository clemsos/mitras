#!/usr/bin/env python
# -*- coding: utf-8 -*-


from gensim import corpora, models, similarities, matutils, interfaces
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from multiprocessing import Pool

from lib.api import Similarity_API

import numpy as np
from time import time
import codecs
import pickle
import os.path

types=["diffusion","tweets","txt","users"]

# MAIN : Step 1
def compute_and_save_similarity_corpus(_path): 

    # STEP 1 
    print 
    print "Step 1 : Compute all vectors from protomemes raw corpus"
    print '#'*40
    print
    
    tstart=time()

    # TODO : use multi processing to improve computing
    # create corpus and dictionaries
    types=["diffusion","tweets","txt","users"]

    for t in types:
        if not has_corpus(_path,t):
            corpus=get_raw_corpus_file(t,_path)
            create_similarity_corpus(corpus,_path,t)
        else:
            print " Diffusion vector corpus already exists %s/%s.mm"%(_path,t)
            print


# Compile corpus and dictionary
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

        # compute number of times in each corpus
        create_frequency_vectors_corpus(_corpus,dictionary,corpus_path)

    # if no dictionary exists, we have to compute dict and corpus
    else:
        # print type(_corpus)
        print " create %s corpus and dictionary"% _type
        
        # create index of values
        dictionary=create_dictionary(_corpus,dic_path)  

        # compute number of times in each corpus
        create_frequency_vectors_corpus(_corpus,dictionary,corpus_path)

# create dictionary (index of each element)
def create_dictionary(_raw_corpus_path,_dic_path):
    print " Creating dictionary for diffusion."
    print ' Indexing...'
    t0 = time()

    _dic_path

    # load if the file already exists
    dictionary = corpora.Dictionary(c.split(", ") for c in open(_raw_corpus_path, 'rb'))
    dictionary.save(_dic_path) # store the dictionary, for future reference
    print " dico saved at %s " % _dic_path

    print " %d unique ids." % len(dictionary.token2id)
    print " done in %fs" % (time() - t0)
    print 
    return dictionary

# compile corpus (vectors number of times each elements appears)
def create_frequency_vectors_corpus(_corpus,_dictionary,_corpus_path):
    print ' Computing frequency vectors'
    t0 = time()

    corpus_path=_corpus_path
    corpus = [_dictionary.doc2bow(t.split(", ")) for t in open(_corpus, 'rb')]
    corpora.MmCorpus.serialize(corpus_path, corpus) # store to disk, for later use
    print " dico saved at %s " % corpus_path

    print " %d records processed." % len(corpus)
    print " done in %fs" % (time() - t0)
    print
    # pprint(corpus)
    # print corpus

# STEP 2 : similarity between corpuses
def compute_cosine_similarities_from_corpus(_path):

    print "Step 2 : Compute cosine similarities from corpus"
    print '#'*40
    print
    
    # modeling and transformation
    # if not os.path.exists(_path+"/tfidf.mm"):
    #     text_corpus_to_tfidf(_path)
    # else:
    #     print " TF-IDF corpus already processed : %s"%(_path+"/tfidf.index")
    #     print

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

    # This is done with TF-IDF
    if not has_indexed_file(_path,"tfidf"):
        print " computing TF-IDF"
        corpus=corpora.MmCorpus(_path+"/txt.mm")

        # train model from corpus
        if not os.path.exists(_path+"/model.tfidf"):
            print ' creating TF-IDF training model'
            tfidf = models.TfidfModel(corpus) 
            tfidf.save(_path+"/model.tfidf")
            print ' TF-IDF training model saved %s'%(_path+"/model.tfidf")
        else :
            print ' loading trained model'
            tfidf = models.TfidfModel.load(_path+"/model.tfidf")

        tfidf_corpus= tfidf[corpus]
        create_tfidf_similarity_index(tfidf_corpus,_path)
    else:
        print " TF-IDF already indexed : %s"%(_path+"/tfidf.index")
        print

# Load corpus and create
def create_similarity_index(_type,_path):
    
    print " creating similarity index %s"%_type
    print " loading corpus from %s"%_path
    corpus=corpora.MmCorpus(_path+"/"+_type+".mm")
    print "",corpus

    # get number of features from dictionnary length
    # if (_type == "txt"):
    #     dic_path=_path+"/txt.dict"
    # else:
    dic_path=_path+"/"+_type+".dict"

    _num_features=len(corpora.Dictionary.load(dic_path))
    print " getting similarity computed for %d"%_num_features
    file_path=_path+"/"+_type+".index"

    # build the index
    index = similarities.Similarity(file_path, corpus, num_features=_num_features) 
    index.save(file_path)

    print " similarities saved as %s"%file_path
    print 

    return index
    # get similarities between the query and all index 
    # sims = index[corpus]
    # corpus_txt=matutils.MmReader(_path+"/text.mm")
    # corpus_twe=matutils.MmReader(_path+"/tweets.mm")

def create_tfidf_similarity_index(_tfidf_corpus,_path):

    print " creating similarity index for txt transfromed with tf-idf"
    # print " loading corpus from %s"%_path
    # corpus=corpora.MmCorpus(_path+"/"+_type+".mm")
    # print "",corpus

    # get number of features from dictionnary length
    # if (_type == "txt"):
    #     dic_path=_path+"/txt.dict"
    # else:

    dic_path=_path+"/txt.dict"

    _num_features=len(corpora.Dictionary.load(dic_path))
    print " getting similarity computed for %d"%_num_features
    file_path=_path+"/tfidf.index"

    # build the index
    index = similarities.Similarity(file_path, _tfidf_corpus, num_features=_num_features) 
    index.save(file_path)

# THIS HAS BEEN MOVED TO THE Similarity API (lib/api.py)
# STEP 3 : Create similarity matrix of all files
# def create_combined_similarities_index(_path):
#     print "Step 3 : Combine similarities index"
#     print '#'*40
#     print 

#     t0=time()

#     # save path
#     combi_path=_path+"/similarities_matrix.npy"
    
#     # api=Similarity_API(_path)

#     # get row count
#     diff_corpus=corpora.MmCorpus(_path+"/diffusion.mm")
#     count=len(diff_corpus)

#     print " Starting linear combination for %d similarity measures"%count
#     print " computing..."

#     # np.memmap(combi_path, dtype='float32', mode='w+', shape=(count,count))
#     # size of this will be 43959*43959*16=28.794 Go

#     # for x in range(0,10):
#     #     print api.get_row(x)
        
#     # with open(combi_path, 'w') as f:
#     #     # f.write(map(str,[x]) for x in range(0,count))
#     #     f.write("\n".join(" ".join(map(str, api.get_row(x))) for x in range(0,count)))

#     print " similarity matrix stored as file : %s"%combi_path
#     print 
#     print " Similarities computation done ",
#     print " in %fs"%(time()-t0)
#     print 

# Utils
def has_corpus(_path,_type):
    corpus_path=_path+'/'+_type+'.mm'
    return os.path.exists(corpus_path)

def has_indexed_file(_path,_type):
    index_path=_path+'/'+_type+'.index'
    return os.path.exists(index_path)

def get_raw_corpus_file(_type,_path):
    filename=_path+"/protomemes."+_type
    if os.path.exists(filename):
        print " loading raw corpus from %s "%filename
        return filename
    else:
        raise ValueError("File is not here. Try to create protomemes corpus files via lib.protomemes.create_corpus_file()")


# TODO :
def compute_similarities_using_multiple_processes(l):
    '''process the test list elements in parallel'''
    
    print '  using multi-process pool'
    pool = Pool()
    results = pool.map(create_similarity_matrix, l)
    return results


