#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import time
from test_helpers import TestHelpers

helpers=TestHelpers()
helpers.add_relative_path()

from lib.api import Similarity_API
from lib.protomemes import create_protomemes_index_file,get_row_by_protomemes,get_protomemes_by_row, get_protomemes_ids_by_rows
from lib.memes import *
import numpy as np
from time import time

import tempfile

path="/home/clemsos/Dev/mitras/data/tmp"

# Create the combined similarities index matrix
chunk_size=2500 # cut the whole dataset into chunks so it can be processed
protomemes_count= 43959 #db["hashtags"].count()
api=Similarity_API(path,protomemes_count,chunk_size)

sims=api.get_similarity_matrix()
# labels=api.get_labels()
print sims.shape

similarity_treshold = 0.7 # minimum value of similarity between protomemes
similar_protomemes_treshold=20
print 'getting rows with %d protomemes that are at least %.0f percent similar'%(similar_protomemes_treshold,similarity_treshold*100)

# get index of row containing enough similar elements
# index_of_rows_containing_memes=np.where( (sims > similarity_treshold).sum(axis=1) >= similar_protomemes_treshold)[0]

# np.save(path+"/index_of_rows_containing_memes.npy",index_of_rows_containing_memes)


t0=time()

index_of_rows_containing_memes=np.load(path+"/index_of_rows_containing_memes.npy")

# rows_containing_memes
rows_containing_memes=sims[index_of_rows_containing_memes]
# print rows_containing_memes.shape

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

# np.where(indexes[rows_containing_memes > similarity_treshold])
# i=get_protomemes_by_row(path,2499)
# print i[0]["_id"]
