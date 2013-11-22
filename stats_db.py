#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.plot import create_bar_graph
from lib.mongo import MongoDB
from time import time
from datetime import datetime
from bson.code import Code
from collections import Counter

collection="week1"

# Connect to Mongo
db=MongoDB("weibodata").db
data=db[collection]
tweets_count=data.count()
print 10*"-"
print "%s tweets in the db"%tweets_count

# Load data
def get_tweets_count_time_series(_collection,_count):
    print
    print "Getting tweets time series"
    print " loading %d tweets from "%_count,
    print "%s db..."%_collection
    print " launching map reduce..."

    t0 = time()
    mapper= Code("""function() {

                    var c=new Date(this.created_at)

                    var day = new Date(c.getFullYear(), c.getMonth(), c.getDate());
            
                emit({day: day}, {count: 1});
            }""")

    reducer=Code( """function(key, values) {
          var count = 0;

          values.forEach(function(v) {
            count += v['count'];
          });

          return {count: count};
        }""")
    
    if _count==0:
        result = data.inline_map_reduce(mapper, reducer)
    else:
        result = data.inline_map_reduce(mapper, reducer, limit=_count)

    # Parse data
    # for r in result.find():
    #     print r
    #     print r["_id"]["day"],
    #     print r["value"]["count"]

    dates=[r["_id"]["day"] for r in result ]
    values=[r["value"]["count"] for r in result ]

    print " done in %fs" % (time() - t0)
    print "%d dates and"%len(dates),
    print "%d values"%len(values)

    return dates,values

def get_tweet_per_user(_collection,_count):

    print
    print "Computing tweet per user from %d tweets "%_count,
    print "in %s db..."%_collection
    print " launching map reduce..."

    t0 = time()
    mapper= Code("""function() {

                    // var c=new Date(this.created_at);

                    // var day = new Date(c.getFullYear(), c.getMonth(), c.getDate());
                    var user = this.userId;
            
                emit({user: user}, {count: 1});
            }""")

    reducer=Code( """function(key, values) {
          var count = 0;

          values.forEach(function(v) {
            count += v['count'];
          });

          return {count: count};
        }""")
    
    if _count==0:
        result = data.inline_map_reduce(mapper, reducer)
    else:
        result = data.inline_map_reduce(mapper, reducer, limit=_count)

    # Parse data
    # for r in result.find():
    #     print r
    #     print r["_id"]["day"],
    #     print r["value"]["count"]

    # dates=[r["_id"]["user"] for r in result ]
    values=[r["value"]["count"] for r in result ]

    print " done in %fs" % (time() - t0)
    # print "%d dates and"%len(dates),
    print " %d values returned"%len(values)

    return values

# Visualize tweets volume by day
# dates,values=get_tweets_count_time_series(data, 10)
# title ='Volume of tweets in '+collection+' by day'
# create_bar_graph(dates,values,title, False)

tweet_per_user=get_tweet_per_user(data, 10000)
print " Number of unique users :  %d "%len(tweet_per_user)
print " Number of unique tweets :  %d "%sum(tweet_per_user)

# group results 
tweet_per_user_counts=Counter(tweet_per_user)
# print tweet_per_user_counts
# for i,c in enumerate(count):
#     print ids[i],c

x=[ tweet_per_user_counts[c] for c in tweet_per_user_counts ]
y=[ c for c in tweet_per_user_counts ]
# print x, y

# Create graph
title ='Number of tweets per users %s'%collection
# create_bar_graph(x,y,title, True)