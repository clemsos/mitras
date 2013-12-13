#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from time import time
from lib.mongo import MongoDB
from models.meme import Meme
import csv
import numpy as np
import tempfile
from protomemes import get_protomemes_ids_by_rows

# Connect to Mongo
db=MongoDB("weibodata").db


def get_meme_list():
    query1 ={}
    query2 = { "name" : 1}
    db_list=db["memes"].find(query1,query2)
    meme_list=[m["name"] for m in db_list]
    return meme_list
    
def create_meme_from_protomemes(_name,_protomemes_ids):

    t0 = time()
    print
    print "Creating meme from protomemes"
    # print " launching map reduce..."
    
    # valid protomemes
    valid_types =["hashtags","mentions","urls","phrase"]

    #collect all tweets id
    tweets=[]
    for collection in _protomemes_ids:

        if collection not in valid_types:
            raise ValueError(" protomeme type not valid %s")%collection

        print " collecting %d protomemes from %s db..."%(len(_protomemes_ids[collection]), collection)

        query={ "_id":  { "$in": _protomemes_ids[collection] } }

        result=list(db[collection].find(query,{ "value.tweets": 1 }))
        for r in result:
            for t in r["value"]["tweets"]:
                tweets.append(t)

    print " %d tweets ids retrieved"%len(tweets)
    print
    print "Getting tweets..."  

    # print type(tweets)
    # print tweets

    query={ "mid":  { "$in": tweets } }
    
    # TODO : change to a normal collection name !
    results=list(db["tweets"].find(query))

    print "Got %d tweets !"%len(results)
    print 
    print "Creating meme"
    meme=Meme()
    meme.name=_name
    meme.tweets=results
    meme.save()
    print "Meme created !"
    print
    print " done in %fs" % (time() - t0)
    # return dates,values

def list_to_csv(_keys,_rows,_csv_filepath):
    
    # get keys for csv value
    # keys=_rows[0].keys()

    print " extracting %s from tweets"%(_keys)
    # write to csv
    with open(_csv_filepath,'w') as f: # writes the final output to CSV
        csv_out=csv.writer(f)
        csv_out.writerow(_keys) # add header
        for row in _rows:
            csv_out.writerow(row)

    print " csv has been stored as %s"%_csv_filepath

def meme_to_gephi_csv(_name,_dir_path):
    # t0=time()

    # get meme data
    query={ "name" : _name}
    meme=list(db["memes"].find(query))[0]
    print " tweets in meme :  %d" % len(meme["tweets"])

    # 
    nodes=[]
    edges=[]

    for i,t in enumerate(meme["tweets"]):
        nodes.append( (t["userId"],"user"+str(i)) )

        # add mentions
        for m in t["mentions"]:
            edges.append((t["userId"],m))
        
        # add RTs
        if t["retweetFromUserId"] != "": 
            edges.append((t["retweetFromUserId"],t["userId"]))

    list_to_csv(["Id", "Label"],nodes,_dir_path + '/'+_name+'_nodes.csv')
    list_to_csv(["Source","Target"],edges,_dir_path +'/'+_name+'_edges.csv')
    print 
    # print " done in %fs" % (time() - t0)

def meme_to_d3_csv(_name,_dir_path):

    pass

def create_meme_index(_tmp_path,_similarity_index,_similar_protomemes_treshold,_similarity_treshold):
  if not os.path.exists(_tmp_path+"/index_of_rows_containing_memes.npy") : 
      # labels=api.get_labels()
      print _similarity_index.shape

      print 'getting rows with %d protomemes that are at least %.0f percent similar'%(_similar_protomemes_treshold,_similarity_treshold*100)


      # get index of row containing enough similar elements
      index_of_rows_containing_memes=np.where( (_similarity_index > _similarity_treshold).sum(axis=1) >= _similar_protomemes_treshold)[0]


      # print type(remarquable_rows)
      print " found %d row containing enough similar elements"%len(index_of_rows_containing_memes)
      print index_of_rows_containing_memes

      np.save(path+"/index_of_rows_containing_memes.npy",index_of_rows_containing_memes)
  else :
      print 
      "Row containing memes already exists %s"%(_tmp_path+"/index_of_rows_containing_memes.npy")

def create_memes(_tmp_path,_similarity_index,_similarity_treshold):
  index_of_rows_containing_memes=np.load(_tmp_path+"/index_of_rows_containing_memes.npy")

  # rows_containing_memes
  rows_containing_memes=_similarity_index[index_of_rows_containing_memes]

  for row in (rows_containing_memes > _similarity_treshold):
    
    # recreate row id 
    similar_protomemes_indexes=np.arange(0,len(row))[row]
    # print type(similar_protomemes_indexes)

    protomemes=get_protomemes_ids_by_rows(_tmp_path,similar_protomemes_indexes)
    
    # print protomemes
    print " %d protomemes"%len(protomemes)
    
    # generate random name
    # TODO : create meaningful name
    meme_name = tempfile.NamedTemporaryFile().name.split('/')[2]

    create_meme_from_protomemes(meme_name,protomemes)