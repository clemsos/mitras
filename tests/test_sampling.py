#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
In a week of data, we find ~700 000 protomemes. 
If we want to compare them, we end up with a similarity matrix of size 700 000 x 700 000 x 32 (this is stored as a np 32-bit array)
This is useless and not realistic (keep in mind we have 52 weeks to process).


We should use with a protomemes set of ~10 000 to start with.
Let's define criterium to sample the protomemes : 

- at least 5 users involved
- at least contains 5 tweets

'''

from time import time
from test_helpers import TestHelpers
import codecs

helpers=TestHelpers()
helpers.add_relative_path()

from lib.mongo import MongoDB

# Connect to Mongo
db=MongoDB("weibodata").db

stats=[
    ("hashtags",44382),
    ("mentions",398392),
    ("urls",264651)
]

results=[]
for collection in stats:
    print "sampling %s from a total %d protomemes"%(collection)
    query={
            # "value.tweets.5":{ "$exists":"true"},
            "value.users.5": { "$exists":"true"}
        }

    res=list(db[collection[0]].find(query))
    results=results+res

print " %d protomemes"%len(results)