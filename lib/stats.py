#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import time
from datetime import datetime
from bson.code import Code

def get_tweets_volume_time_series(_collection,_count):
    print
    print "Getting tweets time series"
    print " loading %d tweets from "%_count
    # print "%s db..."%_collection
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
        result = _collection.inline_map_reduce(mapper, reducer)
    else:
        result = _collection.inline_map_reduce(mapper, reducer, limit=_count)

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

def get_tweet_volume_per_user(_collection,_count):

    print
    print "Computing tweet per user from %d tweets "%_count
    # print "in %s db..."%_collection
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
        result = _collection.inline_map_reduce(mapper, reducer)
    else:
        result = _collection.inline_map_reduce(mapper, reducer, limit=_count)

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
