#!/usr/bin/env python
# -*- coding: utf-8 -*-

from test_helpers import TestHelpers
from time import time
from bson.code import Code

helpers=TestHelpers()
helpers.add_relative_path()
from lib.mongo import MongoDB

# Variables
collection="week1"

# Connect to Mongo
db=MongoDB("weibodata").db
# count = db[collection].count()
count = 10000

t0 =time()

print "Starting map reduce"
# Load map and reduce function from js files
mapper = Code(open("/home/clemsos/Dev/mitras/lib/mapreduce/map.js", "r").read())
reducer = Code(open("/home/clemsos/Dev/mitras/lib/mapreduce/reduce.js", "r").read())

result = db.week1.map_reduce( mapper, reducer, "test", limit=count)
t1=time()-t0
print " done in %fs" % (time() - t0)
print " count :  %d results" % result.count()

# for h in result.find():
    # print h["value"]["users"]
    # print h["value"]["txt"]
    # print h["value"]["diffusion"]
    # print h["value"]["tweets"]


# print count
# # count= 0 #data.count()

# pipeline = [
#         { "$project" : { 
#             "hashtags" : 1,
#             }
#         },
#         { "$limit" : count },
#         { "$unwind" : "$hashtags"} ,
#         { "$group" : {
#             "_id"       : "$hashtags", 
#             } 
#         }
#     ]

# t0 =time()
# q = db.command('aggregate', collection, pipeline=pipeline )

# t1=time()-t0

# hashtags = q["result"]

# print " Data was extracted succesfully in %fs" % (time() - t0)
# print " count :  %d results" % len(hashtags)
# # print " Matrix : n_samples: %d, n_features: %d" % tfidf_matrix.shape
# print

# for h in hashtags:
#    print h