#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from scipy import spatial
import numpy as np
import numpy.random as rand #  RandomState,seed
from time import time
from sklearn.metrics.pairwise import cosine_similarity

import Queue
import threading

from test_helpers import TestHelpers
helpers=TestHelpers()
helpers.add_relative_path()

def generate_matrix(_size):
    print "generate a matrix of shape %s by "%_size,_size
    prng = rand.RandomState(1234567890)
    d=[]
    for a in range(0,_size):
        d.append(prng.randint(0, 10, size=_size))
    return np.array(d)



size=500

d1=generate_matrix(size)
d2=generate_matrix(size)
d3=generate_matrix(size)
a=[d1,d2,d3]

print 'Benchmark cosine similarity w OR w/o threading'
print 

print "Computing cosine without threading..."
t0=time()
for x in a:
    [cosine_similarity(x, pm) for pm in x]

print "done in %fs"%(time()-t0)
print

q = Queue.Queue()


# called by each thread
def compute_cosine(q, x):
    q.put([cosine_similarity(x, pm) for pm in x])

print "Computing cosine with threading..."
t0=time()
for x in a:
    t = threading.Thread(target=compute_cosine, args = (q,x))
    t.daemon = True
    t.start()
s = q.get()
print "done in %fs"%(time()-t0)
print



