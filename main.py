#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.mongo import MongoDB
from lib.protomemes import get_protomemes
from lib.vectorizer import vectorize_text, tdidf, create_dictionary,get_frequency_vectors,create_matrix_from_vectors, cosine_similarity

import numpy as np
from time import time
import pylab
from scipy import array as sparray
from scipy.cluster.hierarchy import linkage, dendrogram,leaves_list
from scipy.cluster.vq import kmeans,vq
from scipy.spatial.distance import pdist, squareform

import matplotlib.pyplot as plt

# Variables
# collection="week1"
# Connect to Mongo
# db=MongoDB("weibodata").db
# count = db[collection].count()

t00=time()

count=60
pms=get_protomemes("hashtags",count)
# convert to numpy array 
protomemes=np.array(pms)

print "%d protomemes obtained." % len(protomemes)
print 

print
print "Label matrix with protomemes description"

labels=[p["value"]["type"] +" : "+p["_id"] for p in protomemes]

print " length of labels %d"%len(labels)

print '#'*40
print "Step 1 : Compute all vectors from protomemes"

##################################################################
# Text similarity (TF-IDF)
#

print '-'*40
print "Computing text vectors from protomemes"
print 

corpus=vectorize_text(protomemes)
text_matrix=tdidf(corpus)

##################################################################
# Diffusion similarity
# 

print '-'*40
print 'Vectorizing diffusion using RT/mentions users list'
print 

print " Creating dictionary for diffusion"
diffusion=[]
for proto in protomemes:
    diffusion.append(proto["value"]["diffusion"])
dictionary=create_dictionary(diffusion)

vector_diffusion_corpus=get_frequency_vectors(diffusion,dictionary)
diffusion_matrix=create_matrix_from_vectors(vector_diffusion_corpus)


##################################################################
# Binary tweets
#

print '-'*40
print "Vectorizing tweets ids"
print

print " Creating dictionary for binary tweets"
binary_tweets=[]
for proto in protomemes:
    binary_tweets.append(proto["value"]["tweets"])

tweet_dic=create_dictionary(binary_tweets)
tweet_corpus=get_frequency_vectors(binary_tweets,tweet_dic)
tweets_matrix=create_matrix_from_vectors(tweet_corpus)

##################################################################
# User similarity
# TODO : add all ids of user to protomemes (should be mined in prepare.py)
#
# print '-'*40
# print "TODO : Tweet simple similarity "
# print 

##################################################################
# STEP 2 
# Compute similarities
#

print "Step 2 : Compare and combine matrix to detect clusters"
print '#'*40
print
print " text_matrix - n_samples: %d, n_features: %d "%text_matrix.shape
print " tweets_matrix - n_samples: %d, n_features: %d "%tweets_matrix.shape
print " diffusion_matrix - n_samples: %d, n_features: %d "%diffusion_matrix.shape
print
print "Compute cosine similarities from corpus"

t0=time()

text_sim=[cosine_similarity(pm, text_matrix)[0] for pm in text_matrix]
diffusion_sim=[cosine_similarity(pm, diffusion_matrix)[0] for pm in diffusion_matrix]
tweets_sim= [cosine_similarity(pm, tweets_matrix) for pm in tweets_matrix]

print " done in %fs" % (time() - t0)

print 
# linear combination of similarity measures,
print "Starting linear combination of similarity measures,"
wt = 0.0
wc = 0.7 
wu = 0.1
wd = 0.2

if wt+wc+wu+wd != 1:
    raise ValueError("scale factors sum should equals 1")

# TODO : add missing parameters
print " weighting and scaling up matrix "
combi=wc*np.array(text_sim) +wd*np.array(diffusion_sim) #+wt*np.array(tweets_sim)
print " combination length :%d " % len(combi)

print " calculate matrix w average linkage algorithm"
linkage_matrix=linkage(combi, method='average')
print " clusters: n_samples: %d, n_features: %d" % linkage_matrix.shape

def explain_clusters(clusters):
    for row in clusters:
        i=int(row[0])
        value1="cluster"
        if i in range(0,len(protomemes)):
            value1=labels[i]    

        j=int(row[0])
        value2="cluster"
        if j in range(0,len(protomemes)):
            value2=labels[j]

        print row
        print "---> [",value1,value2, row[2],"]"


print " get order from dendrogram leaves"
reordered = leaves_list(linkage_matrix)

#reorder the data matrix and row headers according to leaves
ordered_data_matrix = combi[reordered,:]

#do the same for the row headers
row_headers = np.array(labels)
ordered_row_headers = row_headers[reordered,:]

#output data for visualization in a browser with javascript/d3.js
matrixOutput = []
row = 0
for rowData in ordered_data_matrix:
    col = 0
    rowOutput = []
    for colData in rowData:
        rowOutput.append([colData, row, col])
        col += 1
    matrixOutput.append(rowOutput)
    row += 1


# Export to js vars for visualization with d3.js
# BUG : not working
jsfile=""
jsfile+='var maxData = ' + str( np.amax(protomemes) ) + ";"
jsfile+='\n\n'
jsfile+= 'var minData = ' + str(np.amin(protomemes)) + ";"
jsfile+='\n\n'
jsfile+= 'var data = ' + str(matrixOutput) + ";"
jsfile+='\n\n'
jsfile+= 'var cols = ' + str(labels) + ";"
jsfile+='\n\n'
jsfile+= 'var rows = ' + str([x for x in ordered_row_headers]) + ";"

with open('ui/data/data.js', 'w') as myFile:
    myFile.write(jsfile)

print
print " plotting data and generating images"
# use vq() to get as assignment for each obs.
# assignment,cdist = vq(clusters,clusters)
# plt.scatter(clusters[:,0], clusters[:,1], c=assignment)
# plt.show()

# plt.clf()

def augmented_dendrogram(*args, **kwargs):

    ddata = dendrogram(*args, **kwargs)

    if not kwargs.get('no_plot', False):
        for i, d in zip(ddata['icoord'], ddata['dcoord']):
            x = 0.5 * sum(i[1:3])
            y = d[1]
            plt.plot(x, y, 'ro')
            plt.annotate("%.3g" % y, (x, y), xytext=(0, -8),
                         textcoords='offset points',
                         va='top', ha='center')

#     return ddata
# print clusters

# # ss=dendrogram(clusters)
# show_leaf_counts = True
# ddata = augmented_dendrogram(clusters,
#                color_threshold=1,
#                p=60,
#                truncate_mode='lastp',
#                show_leaf_counts=show_leaf_counts,
#                )
# # plt.title("show_leaf_counts = %s" % show_leaf_counts)

# plt.show()

print " everything done in %fs" % (time() - t00)