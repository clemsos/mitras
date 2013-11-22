#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from scipy import spatial
import numpy as np
import numpy.random as rand #  RandomState,seed
from time import time
from sklearn.metrics.pairwise import cosine_similarity

import multiprocessing
from multiprocessing import Pool

from test_helpers import TestHelpers
helpers=TestHelpers()
helpers.add_relative_path()

#generate test data
def generate_matrix(_size):
    print "generate a matrix of shape %s by "%_size,_size
    prng = rand.RandomState(1234567890)
    d=[]
    for a in range(0,_size):
        d.append(prng.randint(0, 10, size=_size))
    return np.array(d)

#worker
def compute_cosine(matrix):
    """worker function"""
    print 'Worker, go compute!'
    t1=time()
    cos=[cosine_similarity(matrix, pm) for pm in matrix]
    # sleep(2)
    print " I am done now",
    print " in %fs"%(time()-t1)
    return cos

# single process
def single(l):
    # process the test list elements using a single process
    results = []
    for sublist in l:
        results.append(compute_cosine(sublist))
    return results

# multi process
def multi(l):
    # process the test list elements in parallel
    pool = Pool()
    results = pool.map(compute_cosine, l)
    return results

size=1000
print "Generating test data"
d1=generate_matrix(size)
d2=generate_matrix(size)
d3=generate_matrix(size)
a=[d1,d2,d3]

print 'Benchmark cosine similarity w OR w/o multiprocesses'
print 

print "Computing cosine without multiprocesses..."
t0=time()
singleresults=single(a)
print "done in %.3fs"%(time()-t0)
print

# print "Computing using Process..."
# p1 = multiprocessing.Process(name="p1",target=compute_cosine,args=(d1,))
# p1.start()
# p2 = multiprocessing.Process(name="p2",target=compute_cosine,args=(d2,))
# p2.start()
# p3 = multiprocessing.Process(name="p3",target=compute_cosine,args=(d3,))
# p3.start()

print "Computing using multiprocessing Pool..."
t0=time()
multiresults=multi(a)
print "done in %.3fs"%(time()-t0)
print

# make sure they both return the same thing
# assert singleresults == multiresults