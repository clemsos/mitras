#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main file showing the whole clustering process in a single file.

"""
import os
from time import time
import numpy as np

from lib.csv2mongo import extract_and_store_tweets

from lib.nlp import NLPMiner
import lib.tweetminer as minetweet

from lib.mongo import MongoDB

from lib.protomemes import extract_protomemes_using_multiple_processes, create_corpus_file_by_type,create_protomemes_index, get_protomemes_ids_by_rows

from lib.vectorizer import compute_and_save_similarity_corpus, compute_cosine_similarities_from_corpus

from lib.api import Similarity_API

from lib.clusters import get_linkage_matrix
from lib.visualizer import create_dendogram
from lib.memes import *

import matplotlib.pyplot as plt

import tempfile


tstart=time()

'''
1. Download and store all files from HKU server
'''

# os.system('wget -r "http://147.8.142.179/datazip/"')

# TODO : scan all downloaded files
# raw_csv_folder=os.path()+"/147.8.142.179/datazip/"
# data_files=[]
# for files in folder(raw_csv_folder) as f:
#   data_files.append(f)

'''
2. Process all tweets in csv file and store to mongoDB
'''
# init libraries
# nlp=NLPMiner()

# for csv_file in data_files:
    # extract_and_store_tweets(csv_file,nlp, minetweet)

'''
3. Extract all protomemes from the tweets corpus
'''
# where the raw data is
collection="tweets"

# Connect to Mongo
db=MongoDB("weibodata").db

# get corpus length
tweets_count=db[collection].count()
print str(tweets_count)+" tweets in the db"
print 10*"-"

# Define elements to extract
# (source, collection, number of items, destination)
collection_args= [
    ("hashtags", collection, tweets_count,"hashtags"),
    ("mentions", collection, tweets_count,"mentions"),
    ("urls", collection, tweets_count,"urls")
    ]

# launch the protomemes extraction
# extract_protomemes_using_multiple_processes(collection_args)

'''
4. Compute protomemes similarities
'''

# Temporary directory to store all indexes
# path="/tmp"
path="/home/clemsos/Dev/mitras/data/tmp"

# Reference different types of corpus
types=["txt","diffusion","tweets","users"]

# Create raw corpus for each protomeme with at least 5 tweets and 5 users
for t in types:
    create_corpus_file_by_type(t,0,path)

# Create index of protomemes
create_protomemes_index(path)

# Convert each corpus to vectors
compute_and_save_similarity_corpus(path)

# Create similarities index for each corpus
compute_cosine_similarities_from_corpus(path)

# Create the combined similarities index matrix
chunk_size=2500 # cut the whole dataset into chunks so it can be processed
protomemes_count= 43959 #db["hashtags"].count()
api=Similarity_API(path,protomemes_count,chunk_size)

if not os.path.exists(path+"/similarity_matrix.npy"):
    print "Create combined matrix"
    api.create_combined_similarities_index(False)
else:
    print "Combined similarity matrix already exists"

'''
5. Identify important clusters in the dataset
'''

similarity_treshold = 0.9 # minimum value of similarity between protomemes
similar_protomemes_treshold=20

sims=api.get_similarity_matrix()

if not os.path.exists(path+"/index_of_rows_containing_memes.npy") : 
    # labels=api.get_labels()
    print sims.shape

    print 'getting rows with %d protomemes that are at least %.0f percent similar'%(similar_protomemes_treshold,similarity_treshold*100)


    # get index of row containing enough similar elements
    index_of_rows_containing_memes=np.where( (sims > similarity_treshold).sum(axis=1) >= similar_protomemes_treshold)[0]


    # print type(remarquable_rows)
    print " found %d row containing enough similar elements"%len(index_of_rows_containing_memes)
    print index_of_rows_containing_memes

    np.save(path+"/index_of_rows_containing_memes.npy",index_of_rows_containing_memes)
else :
    print 
    "Row containing memes already exists %s"%(path+"/index_of_rows_containing_memes.npy")

t0=time()

index_of_rows_containing_memes=np.load(path+"/index_of_rows_containing_memes.npy")

# rows_containing_memes
rows_containing_memes=sims[index_of_rows_containing_memes]

# '''
# 6. Extract memes from protomemes cluters
# '''

# create the list of all memes set
# meme_list=[np.arange(0,len(i))[i] for i in (rows_containing_memes > similarity_treshold)]
# print len(meme_list)


for row in (rows_containing_memes > similarity_treshold):
  
  # recreate row id 
  similar_protomemes_indexes=np.arange(0,len(row))[row]
  print type(similar_protomemes_indexes)

  protomemes=get_protomemes_ids_by_rows(path,similar_protomemes_indexes)
  
  # print protomemes
  print " %d protomemes"%len(protomemes)
  
  # generate random name
  meme_name = tempfile.NamedTemporaryFile().name.split('/')[2]

  create_meme_from_protomemes(meme_name,protomemes)
  
print " done in %fs" % (time() - t0)

# retrieve all protomemes id 
# protomemes=get_protomemes_ids_by_rows(path,protomemes_rows)
# print " %d protomemes"%len(protomemes)

# # create the meme data set
# create_meme_from_protomemes(protomeme[2],protomemes)

# '''
# 7. Process and visualize meme structure
# '''
# # get the name for the query
# meme_name=protomeme[2]

# # create conversational graph data to be used with Gephi
# meme_to_gephi_csv(meme_name,path)

# print
# print " done in %fs" % (time() - t0)
# print ":) "*12
# print