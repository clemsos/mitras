#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gensim import corpora, models, similarities, matutils, interfaces
import numpy as np
from scipy.sparse import *
from time import time
from test_helpers import TestHelpers

helpers=TestHelpers()
helpers.add_relative_path()

from lib.api import Similarity_API
from multiprocessing import Pool

# from csc import divisi2
import scipy.sparse as sparse

def test_get_similarity_matrix_row():
    t0=time()
    for x in range(0,5):
        print api.get_row(x,count)

    print "done in %.3fs"%(time()-t0)
    print

# worker function
def create_matrix_row_by_type(args):
    print " start worker %d"%args[0]
    results=np.zeros(args[1])
    for x in range(0,args[1]):
        results[args[1]-1]=api.get_row_by_type(x,args[0])
    print results
    np.save(open(path+"/"+api.types[args[0]]+".npy", "w"),results)

def test_compute_each_type_without_multiprocess(args):
    t0=time()
    print 
    print '  without multi-process pool'
    for a in args:
        create_matrix_row_by_type(a)
    print "done in %.3fs"%(time()-t0)

def test_compute_each_type_using_multiprocess(args):
    t0=time()
    print 
    print '  using multi-process pool'
    pool = Pool()
    results = pool.map(create_matrix_row_by_type, args)
    print "done in %.3fs"%(time()-t0)

# cpu_count=4
# # test_get_sparse_chunk_of_data(count,chunk_length)
# # for chunk_start in xrange(0, _count, _chunk_length)
# args=[]
# for i,x in enumerate(xrange(0, count, count/cpu_count)):
#     if i != 0 : args.append( ( (i-1)*count/4,x,count ) )
# print args

# gives scipy error as described here 
# http://stackoverflow.com/questions/12113498/valueerror-taking-dot-product-of-two-sparse-matrices-in-scipy
def test_compute_the_whole_corpus():
    results=[]
    count =707425

    matrix=np.zeros([count,count]) # error 
    t0=time()
    print "starting complete computation of all the stuff"
    for i,d in enumerate(api.data):    
        print ' Computing for %s ...'%api.types[i]
        t1=time()
        res = np.zeros(count)
        vec=d[0] # get vectors
        sim=d[1] # get similarity
        
        # add weighted similarity
        res=sim[vec]*api.weights[i]
        print " done in %.3fs"%(time()-t1)
        results.append(res)

    print "everything done in %.3fs"%(time()-t0)
    print

def test_compute_sparse_corpus():
    results=[]
    count =707425

    t0=time()
    print "starting complete computation of all the stuff"
    for i,d in enumerate(api.data):    
        print ' Computing for %s ...'%api.types[i]
        t1=time()
        res = np.zeros(count)
        vec=d[0] # get vectors
        sim=d[1] # get similarity
        
        # add weighted similarity
        res=sim[vec]*api.weights[i]
        print " done in %.3fs"%(time()-t1)
        results.append(res)

    sum(res)
    print "everything done in %.3fs"%(time()-t0)
    print

def test_get_sparse_chunk_of_data(_start,_count,_chunk_length):

    for chunk_start in xrange(_start, _count, _chunk_length):
    # print ' Computing a chunk of  %d values...'%(chunk_length)
        t0=time()
        values=[]
        chunk_end=min(_count, chunk_start + _chunk_length)
        print chunk_start,chunk_end

        # take each type of protomeme
        for i,d in enumerate(api.data):
            corpus=d[0] # get vectors
            sim_index=d[1] # get similarity

            # get all vectors in the range of values
            chunk=[]
            for j in range(chunk_start , chunk_end):
                chunk.append(corpus[j])

            # get similarities values for the chunk    
            sims=sim_index[chunk]
                    
            # weight sims according to the 
            # print sims*api.weights[i]

            # store tmp for linear combination
            values.append(sims)

        # combine of all values
        # combined=sum(values)
        print "  done in %.3fs"%(time()-t0)

        # save chunk of data 
        # matrix_file.write(combined)

def sparse_chunk_worker(_args):
    print " worker, work  ! NOW !"
    test_get_sparse_chunk_of_data(_args[0],_args[1],_args[2])

def test_compute_chunks_using_multiprocess(_args):
    t0=time()
    print 
    print '  using multi-process pool'
    pool = Pool()
    results = pool.map(sparse_chunk_worker, _args)
    print "done in %.3fs"%(time()-t0)

def test_compute_by_chunk(_count,_chunk_length):

    print "starting complete computation of all the stuff"
    t0=time()

    for chunk_start in xrange(0, count, chunk_length):
        
        chunk_end=min(count, chunk_start + chunk_length)
        print ' Computing chunk from  %d to %d...'%(chunk_start,chunk_end)

        api.compute_chunk(_count,chunk_start,chunk_end)

    return
    print " computing done in %.3fs"%(time()-t0)
    print

def test_api_create_combined_similarities_index():
    path="/home/clemsos/Dev/mitras/data/similarities"
    count=5
    args= [(0,count),(1,count),(2,count),(3,count)]

    # treshold=10000
    api=Similarity_API(path)

    # chunk size can be changed according to RAM 
    count=707425 # should be the y dimension of the matrix
    chunk_length=250 

    api.create_combined_similarities_index(count,chunk_length)

count =707425
chunk_length=20
# test_compute_by_chunk(count,chunk_length)


t0=time()
path="/home/clemsos/Dev/mitras/data/tmp"
api=Similarity_API(path,count,chunk_length)

test_path="/tmp/row.npy"
# api.get_row_from_file(502)


def create_test_row():
    data=api.get_chunk(1)
    np.save(test_path,data[0])

def load_test_raw():
    return np.load(test_path)

data=load_test_raw()
print data.shape
print data
# print data[0]

d=csr_matrix(data)
print d.shape
# print len(find(d)[0])
d2=csr_matrix(data)
print d2.todense().shape
# h=hstack( [d,d2] ).todense()
# print h.shape

print 
print "done in %.3fs"%(time()-t0)




# combine similarities
# count=707425 # should be the y dimension of the matrix
# chunk_length=250 
# api=Similarity_API(path,count,chunk_length)

# diff_corpus=corpora.MmCorpus(_path+"/diffusion.mm")
# count=len(diff_corpus)
# print " Starting linear combination for %d similarity measures"%count

# chunk size can be changed according to RAM 
# api.create_combined_similarities_index()

# values= [(count,x) for x in range(0, len(api.types))]
# print values
# api.compute_similarities_using_multiple_processes(values)
# api.create_combined_similarities_index(path)