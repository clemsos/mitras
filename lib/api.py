#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gensim import corpora, models, similarities, matutils, interfaces
import numpy as np
from vectorizer import get_raw_corpus_file

class Similarity_API:

    def __init__(self,_path):

        # scalars for linear combination optimization
        w_diffusion = 0.2
        w_tweets = 0.0
        w_users = 0.1
        w_text = 0.7 

        # add scalars -- in the right order please!
        # ["diffusion","tweets","users","text"]
        self.weights=[w_diffusion,w_tweets,w_users,w_text]
        self.data=[] # store vector corpus and similarities measures
        
        # start with 3 easy types
        self.types=["diffusion","tweets","users"]
        for t in self.types:
            self.data.append((  
                    corpora.MmCorpus(_path+"/"+t+".mm"),
                    similarities.Similarity.load(_path+"/"+t+".index")
                    ))
        # add text (separated because of the tfidf specificity)
        self.types.append("text")
        self.data.append((  
                corpora.MmCorpus(_path+"/txt.mm"),
                similarities.Similarity.load(_path+"/tfidf.index"),
                # interfaces.TransformedCorpus.load(_path+"/tfidf.corpus")
                # open(get_raw_corpus_file("txt",_path),"r").readlines(), 
                )) 


    def get_a_row(self,x):
        
        row=[]
        # for each type of protomemes
        for i,d in enumerate(self.data):
            vec=d[0] # get vectors
            sim=d[1] # get similarity
            # add weighted similarity
            row.append(sim[vec[x]]*self.weights[i])

        # proceed to linear combination
        return sum(row)
