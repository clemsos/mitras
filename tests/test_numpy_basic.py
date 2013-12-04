#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

length=16
chunk_length=4
types=["txt","diffusion","tweets","users"]

indices=[0.2,0.3,0.4,0.6]

matrix_path="/tmp/matrix.npy"
final_matrix=np.memmap(matrix_path,dtype='float16', mode='w+', shape=(16,16))

# loop to meet each chunk
for i,x in enumerate(xrange(0,length,chunk_length)):
    
    # init the chunk
    chunk=np.zeros([chunk_length,length])

    # for each type, get chunk and proceed to linear combination
    for c in range(0,len(types)):
        # get a chunk of rows from each
        print " computing similarity for %s with scalar %s "%(types[c],str(indices[c]))
        scalar=indices[c]
        
        chunk+=np.random.random([chunk_length,length])*scalar

    print   

    final_matrix[x:x+chunk_length]+=chunk
    print " chunk added"
print final_matrix.shape

loaded_matrix=np.memmap(matrix_path,dtype='float16', mode='r', shape=(16,16))
print np.amax(loaded_matrix)