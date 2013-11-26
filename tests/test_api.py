#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This is a test for db interactions
'''
from test_helpers import TestHelpers
from time import time

helpers=TestHelpers()
helpers.add_relative_path()

from lib.mongo import MongoDB

# Variables
collection="hashtags"
protoname="吴奇隆"
count = 1000

# Connect to Mongo
db=MongoDB("weibodata").db
# count = db[collection].count()

t0 =time()
print "Requesting all tweets for protomeme : %s"% protoname

query ={ "_id" : protoname }
results=db[collection].find(query).limit(count)

for r in results:
    print r["value"]["diffusion"]

print " results %d"%results.count()
# print " containing %d tweets"%len(results["value"]["tweets"])
print " done in %.3f"%(t0-time())

