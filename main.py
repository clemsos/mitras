#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main file showing the whole clustering process in a single file.

"""
import os
from time import time

from lib.csv2mongo import extract_and_store_tweets
from lib.nlp import NLPMiner
import lib.tweetminer as minetweet
from lib.mongo import MongoDB
from lib.protomemes import extract_protomemes_using_multiple_processes, create_corpus_file_by_type,create_protomemes_index, get_protomemes_ids_by_rows
from lib.vectorizer import compute_and_save_similarity_corpus, compute_cosine_similarities_from_corpus
from lib.api import Similarity_API
from lib.clusters import get_linkage_matrix
from lib.visualizer import create_dendogram, get_graph_csv_filenames, create_network_graph
from lib.memes import *


tstart=time()

# Where are the downloaded raw files
raw_path=os.path.dirname(os.path.abspath(__file__)) +"/data/datazip/"

# Temporary directory to store all indexes
tmp_path="/home/clemsos/Dev/mitras/data/tmp" # tmp_path="/tmp"

# Where should go the final results and outcomes (visualization)
out_path="/home/clemsos/Dev/mitras/data/out"

# Connect to Mongo
db=MongoDB("weibodata").db

# where the raw data is
collection="tweets"

# get corpus length
tweets_count=db[collection].count()
print str(tweets_count)+" tweets in the db"
print 10*"-"


'''
1. Download and store all files from HKU server
'''
# download files
# os.system('wget -r "http://147.8.142.179/datazip/"')

'''
2. Process all tweets in csv file and store to mongoDB
'''
# init libraries
# nlp=NLPMiner()

# scan all downloaded files
csvfiles = [ os.path.join(raw_path,f) for f in os.listdir(raw_path) if os.path.isfile(os.path.join(raw_path,f)) ]

# for csv_file in csv_files:
    # extract_and_store_tweets(csv_file,nlp, minetweet)

'''
3. Extract all protomemes from the tweets corpus
'''

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

# Reference different types of corpus
types=["txt","diffusion","tweets","users"]

# Create raw corpus for each protomeme with at least 5 tweets and 5 users
for t in types:
    create_corpus_file_by_type(t,0,tmp_path)

# Create index of protomemes
create_protomemes_index(tmp_path)

# Convert each corpus to vectors
compute_and_save_similarity_corpus(tmp_path)

# Create similarities index for each corpus
compute_cosine_similarities_from_corpus(tmp_path)

# Create the combined similarities index matrix
chunk_size=2500 # cut the whole dataset into chunks so it can be processed
protomemes_count= 43959 #db["hashtags"].count()
api=Similarity_API(tmp_path,protomemes_count,chunk_size)

if not os.path.exists(tmp_path+"/similarity_matrix.npy"):
    print "Create combined matrix"
    api.create_combined_similarities_index(False)
else:
    print "Combined similarity matrix already exists"

'''
5. Identify important clusters in the dataset
'''

similarity_treshold = 0.9 # minimum value of similarity between protomemes
similar_protomemes_treshold=20

# load the complete similarity matrix
similarity_index=api.get_similarity_matrix()

# create rows containing remarquable memes
create_meme_index(tmp_path,similarity_index,similar_protomemes_treshold,similarity_treshold)

'''
 6. Extract memes from protomemes cluters
'''

create_memes(tmp_path,similarity_index,similarity_treshold)

'''
 7. Process and visualize meme structure
'''

# get the name for the query
meme_list =get_meme_list()
# print meme_list

# create conversational graph data (to be used with Gephi)
# TODO : check for CSV files
if os.path.exists(out_path+"*.csv"):
  for meme_name in get_meme_list():
      meme_to_gephi_csv(meme_name,out_path)    


data = get_graph_csv_filenames(out_path)
create_network_graph(out_path,data)

# print
# print " done in %fs" % (time() - t0)
# print ":) "*12
# print