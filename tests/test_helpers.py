#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import time

class TestHelpers:
    def __init__(self):
        print "loading test helpers..."

    def add_relative_path(self):
        from os import sys, path
        root_path=path.dirname(path.dirname(path.abspath(__file__)))
        print "'" + root_path+"' added to path"
        sys.path.append(root_path)
        # sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

    def load_tweets(self, collection, qty):
        
        t0 = time()

        # import libs
        self.add_relative_path()
        from lib.mongo import MongoDB

        # Connect to Mongo
        db=MongoDB("weibodata").db
        data=db[collection]
        tweets_count=data.count()
        print 10*"-"
        print str(tweets_count)+" tweets in the db"

        # Load data
        print "Loading "+str(qty)+" tweets from "+collection+" db..."
        _type="dico"
        query={_type: {"$not": {"$size": 0} } }
        tweets=data.find(query).limit(qty)

        print "loaded in %0.3fs" % (time() - t0)

        return list(tweets)

