#!/usr/bin/env python
# -*- coding: utf-8 -*-

import lib.protomemes as protomemes
# from lib.mongo import MongoDB

# Connect to Mongo
# db=MongoDB("weibodata").db
# week1=db["week1"]

# count=1000
# count=week1.count()
# print str(count)+" tweets in the db"
# print 10*"-"

protomemes.build_corpus("hashtags", week1, count,"hashtags")
protomemes.build_corpus("mentions", week1, count,"mentions")
protomemes.build_corpus("urls", week1, count,"urls")