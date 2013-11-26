#!/usr/bin/env python
# -*- coding: utf-8 -*-

import lib.protomemes as protomemes
from lib.mongo import MongoDB
from time import time
from multiprocessing import Pool

# Connect to Mongo
db=MongoDB("weibodata").db

count=db["week1"].count()
print str(count)+" tweets in the db"
print 10*"-"


t0=time()

collection_args= [
    ("hashtags", "week1", count,"hashtags"),
    ("mentions", "week1", count,"mentions"),
    ("urls", "week1", count,"urls")
    ]

def extract_protomemes_using_multiple_processes(l):
    '''Process the test list elements in parallel'''    
    print ' creating multi-process pool'
    pool = Pool()
    results = pool.map(pool_proto, l)
    # return results

def pool_proto(args):
    print ' worker : protomemes extraction started for %s'%args[0]
    # print 
    protomemes.build_corpus(args[0],args[1],args[2],args[3])

extract_protomemes_using_multiple_processes(collection_args)