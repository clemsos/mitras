#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gensim import corpora, models, similarities, matutils, interfaces
import numpy as np
from time import time
# from vectorizer import get_raw_corpus_file

class Similarity_API:

    def __init__(self,_path,_treshold):
        self.path=_path
        print 'Loading Similarity API'
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
        print ' all corpus loaded for', self.types

        for d in self.data:
            d[1].num_best = _treshold

    def get_row(self,x,_length):
        
        row=[]
        print " get row %d"%x
        # for each type of protomemes
        # print self.data
        for i,d in enumerate(self.data):
            # print i,d
            vec=d[0] # get vectors
            sim=d[1] # get similarity
            # print vec,sim
            # add weighted similarity
            row.append(sim[vec[x]]*self.weights[i])
            # print self.weights[i]
            # print sim[vec[x]]*0.5

        # proceed to linear combination
        return sum(row)

    def get_row_by_type(self,x,i):
        t0=time()

        vec=self.data[i][0] # get vectors
        sim=self.data[i][1] # get similarity

        # file path to save 
        path=self.path[i]+"/"+self.types[i]+".matrix"

        # get count
        # for x in range(0,count):
        print sim[vec[x]]*self.weights[i]
        
        # add weighted similarity
        # with open(path, 'w') as f:
        #     f.write(map(str,[x]) for x in range(0,count))
        #     f.write("\n".join(" ".join(map(str, api.get_row(x))) for x in range(0,count)))

        # row.append(sim[vec[x]]*self.weights[i])

        # print " storing similarity matrix as file : %s"%combi_path
        # print 
        # print " Similarities computation done ",
        # print " in %fs"%(time()-t0)
        # print 

    def compute_similarities_using_multiple_processes(self,l):
        '''process the test list elements in parallel'''
        
        print '  using multi-process pool'
        pool = Pool()
        results = pool.map(self.create_weighted_matrix, l)
        return results

    def create_combined_similarities_index(self,_path):
        
        t0=time()

        # get row count
        diff_corpus=corpora.MmCorpus(_path+"/diffusion.mm")
        count=len(diff_corpus)

        print " Starting linear combination for %d similarity measures"%count
        print " computing..."
        for x in range(0,10):
            print self.get_row(x)
            
        # with open(combi_path, 'w') as f:
        #     f.write(map(str,[x]) for x in range(0,count))
            # f.write("\n".join(" ".join(map(str, api.get_row(x))) for x in range(0,count)))

        # print " storing similarity matrix as file : %s"%combi_path
        # print 
        # print " Similarities computation done ",
        # print " in %fs"%(time()-t0)
        # print 

class Protomemes_API:
    def __init__(self):
        pass

    def get_protomemes_labels(self,_path):
        labels_path=_path+"/labels.txt"
        print " extracting labels from file : %s"%labels_path
        outfile=open(labels_path,"rb")
        labels=pickle.load(outfile)
        print
        return labels