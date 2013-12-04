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

    # compute similarities of a protomeme with others
    def get_computed_single_row(self,x):
        
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

    # def get_row_by_type(self,x,i):
    #     t0=time()

    #     vec=self.data[i][0] # get vectors
    #     sim=self.data[i][1] # get similarity

    #     # file path to save 
    #     path=self.path[i]+"/"+self.types[i]+".matrix"

    #     # get count
    #     # for x in range(0,count):
    #     print sim[vec[x]]*self.weights[i]
        
    #     # add weighted similarity
    #     # with open(path, 'w') as f:
    #     #     f.write(map(str,[x]) for x in range(0,count))
    #     #     f.write("\n".join(" ".join(map(str, api.get_row(x))) for x in range(0,count)))

    #     # row.append(sim[vec[x]]*self.weights[i])

    #     # print " storing similarity matrix as file : %s"%combi_path
    #     # print 
    #     # print " Similarities computation done ",
    #     # print " in %fs"%(time()-t0)
    #     # print 

    # get a specific row from *.npy
    def get_single_row_from_file(self,x):

        # get path
        chunk=self.get_file_range(x)
        filename="/similarities-%d-%d.npy"%chunk
        combi_path=self.path+filename

        # get the exact index in the file
        row_number=x-chunk[0]


        # load the data
        n=np.memmap(combi_path, mode="r")
        print n

        # return row
        return n[row_number]
        
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

    def create_combined_similarities_index(self, _store_chunks):
        '''
        This function is the main similarity computation function that will create the final matrix with all protomemes paired and their values combined
        
        *
        _store_chunks : Boolean. 
            True will store each separate file
            False will create a single index file

        '''
        
        tstart=time()
        print "Starting complete computation of the similarity matrix"

        # store into multiple files (each of the size of a chunk)
        if _store_chunks is True:

            for chunk_start in xrange(0, self.count, self.chunk_length):
                
                chunk_end=min(self.count, chunk_start + self.chunk_length)
                print ' Computing chunk from  %d to %d...'%(chunk_start,chunk_end)

                self.compute_similarity_chunk(self.count,chunk_start,chunk_end)

        # create a single file with the complete matrix (RAM RAM RAM !)
        else :

            combi_path=self.path+"/similarity_matrix.npy"
        
            # init array for faster processing
            final_matrix=np.memmap(combi_path, dtype='float16', mode='w+', shape=(self.count,self.count))

            # loop to meet each chunk
            for i,x in enumerate(xrange(0,self.count,self.chunk_length)):
                t0=time()
                
                # init the chunk
                chunk=np.zeros([self.chunk_length,self.count])

                # for each type, get chunk and proceed to linear combination
                for c,d in enumerate(self.data):
                    
                    # assign the right corpus
                    corpus=d[0] # get vectors
                    similarity_index=d[1] # get similarity
                    scalar=self.weights[c]

                    # get a chunk of rows from each
                    print " computing similarity for %s with scalar %s "%(self.types[c],str(scalar))
                    
                    sample=[]
                    for n in range(x,x+self.chunk_length):
                        sample.append(corpus[n])

                    print len(sample)
                    chunk+=similarity_index[sample]*scalar

                print  chunk 
                print   

                if self.length-x > self.chunk_length:
                    final_matrix[x:x+self.chunk_length]+=chunk
                else:
                    final_matrix[x:self.length-x]+=chunk

                final_matrix[x:x+self.chunk_length]+=chunk
                final_matrix.save()
                print " chunk processed in %fs"%(time()-t0)
        
        # print 
        print " Similarities matrix stored as file : %s"%combi_path
        print " done in %fs"%(time()-tstart)
        print 

        # return combi_path

    def get_similarity_matrix(self):
        combi_path=self.path+"/similarity_matrix.npy"
        print ' Loading similarity matrix from %s'%combi_path
        return np.memmap(combi_path, dtype='float16', mode='r', shape=(self.count,self.count))


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