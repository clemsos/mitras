#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import time
from test_helpers import TestHelpers

helpers=TestHelpers()
helpers.add_relative_path()

from lib.api import Similarity_API
from lib.protomemes import create_protomemes_index_file,get_row_by_protomemes,get_protomemes_ids_by_rows
from lib.memes import *

path="/home/clemsos/Dev/mitras/data/tmp"
# create_protomemes_index_file(path)
api=Similarity_API(path,707425,250)

protomeme=(path,"hashtags", '吴奇隆')

# get a specific protomeme from the corpus
# i=get_row_by_protomemes(protomeme)

i=278393
print type(i) # 278393

# get index row with all similar elements 
row=api.get_row(i)
print type(row)
print "*%d results"%len(row)
# print row

# similarity treshold
treshold=0.5
print row.shape

# similarity_indexes=[x for i,x in enumerate(row) if x > treshold]
# print " %d similar protomemes (by index)"%len(similarity_indexes)
# print similarity_indexes

similar_protomemes_rows=[i for i,x in enumerate(row) if x > treshold]
# print similar_protomemes
print " %d similar protomemes (by id)"%len(similar_protomemes_rows)

# protomemes=get_protomemes_by_row("/tmp",row)    
# get_protomemes_by_index_rows(similar_protomemes_rows)
protomemes=get_protomemes_ids_by_rows(path,similar_protomemes_rows)
# print protomemes
print " %d protomemes"%len(protomemes)

create_meme_from_protomemes(protomeme[2],protomemes)