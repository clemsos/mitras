#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gensim import corpora, models, similarities, matutils, interfaces
import numpy as np
from time import time
# from vectorizer import get_raw_corpus_file

class Similarity_API:

    def __init__(self,_path,_count,_chunk_length):

        self.path=_path

        # TODO :should be initialize in the constructor
        self.chunk_length=_chunk_length 
        self.length= _count # this value also named _count somewhere else
        self.count= _count

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

    def get_row(self,x):
        
        row=np.zeros([self.length])
        print "get row %d"%x

        # for each type of protomemes
        for i,d in enumerate(self.data):
            corpus=d[0] # get vectors
            similarity_index=d[1] # get similarity

            # add weighted similarity
            row+= similarity_index[corpus[x]]*self.weights[i]

        # proceed to linear combination
        return row

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

    def get_row_from_file(self,x):

        # get path
        r=self.get_file_range(x)
        fn="/similarities-%d-%d.npy"%r
        combi_path=self.path+fn
        print combi_path
        row=x-r[0]#chunk_start
        
        # load
        n=np.load(open(combi_path, "r"))
        print n[row]

    def get_file_range(self,x):
        chunk_start=0
        for c in xrange(0,self.length,self.chunk_length):
            chunk_start=c
            if x in range(chunk_start,chunk_start+self.chunk_length) :
                return (chunk_start,chunk_start+self.chunk_length) 

    def get_chunk(self,x):
        # get path
        r=self.get_file_range(x)
        fn="/similarities-%d-%d.npy"%r
        combi_path=self.path+fn
        print combi_path

        # load
        n=np.load(combi_path, mmap_mode='r')
        return n

    def compute_similarity_chunk(self,_count,_chunk_start,_chunk_end):

        t0=time()
        combi_path=self.path+"/similarities-"+str(_chunk_start)+"-"+str(_chunk_end)+".npy"
        
        # init array for faster processing
        # result=np.zeros([_chunk_end-_chunk_start,_count]) 
        result=np.memmap(combi_path, dtype='float16', mode='w+', shape=(_chunk_end-_chunk_start,_count))

        # each type of similarity
        for i,d in enumerate(self.data): 

            # print " computing for %s"%api.types[i]
            corpus=d[0] # get vectors
            similarity_index=d[1] # get similarity
            
            chunk=[]
            for j in range(_chunk_start , _chunk_end):
                chunk.append(corpus[j])

            # add weighted similarity
            result+=similarity_index[chunk]*self.weights[i]

        # save chunk as a npy array
        # np.save(open(combi_path, "w"),result)
        # result

        print " chunk done in %.3fs"%(time()-t0)
        print " storing similarity matrix as file : %s"%combi_path
        return 

    def create_combined_similarities_index(self):
        
        t0=time()
        print "starting complete computation of all the stuff"
        t0=time()

        for chunk_start in xrange(0, self.count, self.chunk_length):
            
            chunk_end=min(self.count, chunk_start + self.chunk_length)
            print ' Computing chunk from  %d to %d...'%(chunk_start,chunk_end)

            self.compute_similarity_chunk(self.count,chunk_start,chunk_end)

        return
        print " computing done in %.3fs"%(time()-t0)
        print

        # get row count
        # diff_corpus=corpora.MmCorpus(_path+"/diffusion.mm")
        # count=len(diff_corpus)

        # print " Starting linear combination for %d similarity measures"%count
        # print " computing..."
        # for x in range(0,10):
        #     print self.get_row(x)
            
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