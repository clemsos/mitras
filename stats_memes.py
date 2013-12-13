#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from lib.plot import create_bar_graph
from lib.mongo import MongoDB

from time import time
from bson.code import Code
from collections import Counter


# Connect to Mongo
collection="memes"
memes_count = 20

db=MongoDB("weibodata").db
data=db[collection]
total_memes_count=data.count()
print 10*"-"
print "%s memes in the db"%total_memes_count
print


memes = list(data.find().limit(memes_count))

hash=[]
print hash
# print len(memes)
for i, meme in enumerate(memes):
    hash_row= [] 
    # hash[i]=""
    print len(meme["tweets"])
    print "-"*25
    for tweet in meme["tweets"]:
        # print tweet["txt"].encode("utf-8")
        if len(tweet["hashtags"])!=0: 
            for h in tweet["hashtags"]: 
                if h not in hash:
                    hash_row.append(h)
                # print h.encode("utf-8")
    hash.append(hash_row)
    # print "number of unique hashtags: %d"%len(hash_row)

seen = set()
repeated = set()
for l in hash:
  for i in set(l):
    if i in seen:
      repeated.add(i)
    else:
      seen.add(i)

print "number of unique hashtags : %d"%len(seen)
print "number of repeated hashtags : %d"%len(repeated)
