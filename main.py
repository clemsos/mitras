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
from lib.protomemes import extract_protomemes_using_multiple_processes, create_corpus_file_by_type
# from lib.protomemes import get_protomemes, create_txt_corpus_file,create_corpus_file

from lib.vectorizer import compute_and_save_similarity_corpus, compute_cosine_similarities_from_corpus

from lib.api import Similarity_API
from lib.memes import *

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
count=db[collection].count()
print str(count)+" tweets in the db"
print 10*"-"

# Define elements to extract
# (source, collection, number of items, destination)
collection_args= [
    ("hashtags", collection, count,"hashtags"),
    ("mentions", collection, count,"mentions"),
    ("urls", collection, count,"urls")
    ]

# launch the protomemes extraction
extract_protomemes_using_multiple_processes(collection_args)

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

# Convert each corpus to vectors
compute_and_save_similarity_corpus(path)

# Create similarities index for each corpus
compute_cosine_similarities_from_corpus(path)

'''
5. Identify important clusters in the dataset
'''

# chunk_size=250 # cut the whole dataset into chunks so it can be processed
# api=Similarity_API(path,count,chunk_size)

# # TODO !!!!
# # print " calculate matrix w average linkage algorithm"
# # linkage_matrix=linkage(combi, method='average')
# # print " clusters: n_samples: %d, n_features: %d" % linkage_matrix.shape

# # here is a basic example of the process

# # select a protomeme
# protomeme=(path,"hashtags", '吴奇隆')

# # get his index position in the corpus
# i=get_row_by_protomemes(protomeme)

# # get all similar elements
# row=api.get_row(i)
# print "*%d results"%len(row)

# # retrieve all similar elements beyond a treshold
# treshold=0.5
# protomemes_rows=[i for i,x in enumerate(row) if x > treshold]

# protomemes_rows.append(i) #add original protomemes to the set

# print " %d similar protomemes (by id)"%len(similar_protomemes_rows)

# '''
# 6. Extract memes from protomemes cluters
# '''

# # retrieve all protomemes id 
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