#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import time
from lib.mongo import MongoDB
from models.meme import Meme

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