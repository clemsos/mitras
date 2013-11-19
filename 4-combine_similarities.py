#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from numpy import vstack,array
from numpy.random import rand
from time import time
from pprint import pprint

import pandas as pd

import pylab
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.cluster.vq import kmeans,vq
from scipy.spatial.distance import pdist, squareform
from matplotlib import pyplot

# from sklearn.cluster import AgglomerativeClustering

##################################################################
# STEP 2 
# Compute similarity

print '#'*40
print "Step 2 : Combine similarities from the corpus"

number_records=100

matrix={}
matrix["users"]=rand(number_records,number_records)
matrix["text"]=rand(number_records,number_records)
matrix["tweets"]=rand(number_records,number_records)
matrix["spread"]=rand(number_records,number_records)

matrix_indexes=["users","text","tweets","spread"]
# print users_matrix

print type(matrix["users"])
print "All records should be equal size"
print "users_matrix:%d - "  % len(matrix["users"]),
print "text_matrix:%d - "   % len(matrix["text"]),
print "tweets_matrix:%d - " % len(matrix["tweets"]),
print "spread_matrix:%d " % len(matrix["spread"])

# pairwise maximization strategy 
# MAX(Pi,Pj) = max k {Sk(Pi,Pj)}
# for i in range(number_records):
    
#     max_values=[]

#     # find the highest value of similarity in different matrix
#     for m in matrix:
#         max_values.append(max(matrix[m][i]))

#     # define 
#     MAX=max_values.index(max(max_values))
#     print matrix_indexes[MAX]




# linear combination of similarity measures,
wt = 0.0
wc = 0.7 
wu = 0.1
wd = 0.2

if wt+wc+wu+wd != 1:
    print "ERROR : scale factors sum should equals 1"

combi=wu*matrix["users"]+wt*matrix["text"]+matrix["tweets"]+wd*matrix["spread"]

print len(combi)
# Compute 
# TODO : change method to "average"
clusters=linkage(combi, method='average')
# print clusters.shape


# Plot dendrogram.
############
# fig = pylab.figure(figsize=(5,5))
# dendrogram(clusters, 
#            color_threshold=0.3, 
#            # leaf_label_func=lambda x: 'O' * (actlabels.labels[x] + 1),
#            leaf_font_size=6)
# fig.show()
# fig.savefig('dendrogram.png')

# K-Means : Plot variance for each value for 'k' between 1,10
# http://stats.stackexchange.com/questions/9850/how-to-plot-data-output-of-clustering
############
# initial = [kmeans(clusters,i) for i in range(1,10)]
# pyplot.plot([var for (cent,var) in initial])
# pyplot.show()
# cent, var = initial[3]
# print cent
# print var

# #use vq() to get as assignment for each obs.
assignment,cdist = vq(clusters,clusters)
pyplot.scatter(clusters[:,0], clusters[:,1], c=assignment)
pyplot.show()

# Cluster plot
############
# #use vq() to get as assignment for each obs.
# assignment,cdist = vq(clusters,12)
# pyplot.scatter(clusters[:,0], clusters[:,1], c=assignment)
# pyplot.show()

# pylab.plot(clusters) 
# pylab.show()


# Plot colorbar.

# some plotting using numpy's logical indexing
# plot(data[idx==0,0],data[idx==0,1],'ob',
#      data[idx==1,0],data[idx==1,1],'or',
#      data[idx==2,0],data[idx==2,1],'og') # third cluster points
# plot(centroids[:,0],centroids[:,1],'sm',markersize=8)
# show()

# plot(clusters)
# show()

# for i,u in enumerate(users_matrix):
#     print i,len(u)
#     sim=cosine_similarity(u, users_matrix)
#     for s in sim:
#         for j,a in enumerate(s):
#             if a >0:
#                 print str(i)+'-'*40+str(j)
#                 print a
#                 print users[i]
#                 print users[j]