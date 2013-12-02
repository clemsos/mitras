#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import time
from lib.mongo import MongoDB
from models.meme import Meme
import csv

# Connect to Mongo
db=MongoDB("weibodata").db


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

    print type(tweets)

    query={ "mid":  { "$in": tweets } }
    
    # TODO : change to a normal collection name !
    results=list(db["week1"].find(query))

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
    t0=time()

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
            edges.append((t["userId"],t["userId"]))
        
        # add RTs
        if t["retweetFromUserId"] != "": 
            edges.append((t["retweetFromUserId"],t["userId"]))

    list_to_csv(["Id", "Label"],nodes,_dir_path + '/'+_name+'_nodes.csv')
    list_to_csv(["Source","Target"],edges,_dir_path +'/'+_name+'_edges.csv')

    print " done in %fs" % (time() - t0)
