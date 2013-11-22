#!/usr/bin/env python
# -*- coding: utf-8 -*-

from test_helpers import TestHelpers

helpers=TestHelpers()
helpers.add_relative_path()

from lib.protomemes import get_protomemes, build_corpus

import unittest

# t00=time()
# print helpers.load_tweets("week1",1)
class TestSequenceFunctions(unittest.TestCase):

count=20000
proto=get_protomemes("hashtags",count)

# print "%d protomemes obtained." % len(protomemes)
# print 

# db=MongoDB('weibodata').db
# from lib.mongo import MongoDB

coll="week1"

# proto = build_corpus("hashtags",coll,2000, None)

print len(proto)
for p in proto:
    print "*"*12
    try :
        print p["_id"]
        print p["value"]["type"]
    except KeyError:
        print "                  error"
        # print p["_id"]


