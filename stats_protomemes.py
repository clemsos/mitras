#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from lib.plot import create_bar_graph
from lib.mongo import MongoDB

from time import time
from bson.code import Code
from collections import Counter


# Connect to Mongo
collection="hashtags"

db=MongoDB("weibodata").db
data=db[collection]
tweets_count=data.count()
print 10*"-"
print "%s protomemes in the db"%tweets_count
print
print "number of items per hastags" 

def get_hashtags_stats(_collection, _count):
    mapper= Code("""function() {

                    var nbUsers = this.value.users.length;
                    var nbActions = this.value.diffusion.length
                    var nbTweets = this.value.tweets.length
            
                emit({hashtag: this._id}, {users: nbUsers, actions:nbActions, tweets:nbTweets});
            }""")

    reducer=Code( """function(key, values) {
          var countUsers=0;
          var countTweets=0;

          values.forEach(function(v) {
            countUsers += v['users'];
            countTweets += v['tweets'];
            countActions += v['actions'];

          });

          return {users:countUsers, actions:countActions, tweets:countTweets};
        }""")
    
    if _count==0:
        result = _collection.inline_map_reduce(mapper, reducer)
    else:
        result = _collection.inline_map_reduce(mapper, reducer, limit=_count)

    return result

def print_hashtag(h):
    print " users : %d "%h["value"]["users"],
    print " actions : %d "%h["value"]["actions"],
    print " tweets : %d"%h["value"]["tweets"],
    print " ", h["_id"]["hashtag"].encode('utf-8')

t0 = time()
values=get_hashtags_stats(data,0)

# by_users = sorted(values.iteritems(), key=operator.itemgetter(1))

# for hashtag in values:
#     print_hasthag(hashtag)
    
print 
print "Sorting list"
print

winners_count= 50

values_by_user = sorted(values, key=lambda k: k["value"]['users'],reverse=True) 
print "Winners : most users"
for hashtag in values_by_user[0:winners_count]:
    print_hashtag(hashtag)

values_by_actions = sorted(values, key=lambda k: k["value"]['actions'],reverse=True) 
print
print "Winners : most actions"
for hashtag in values_by_actions[0:winners_count]:
    print_hashtag(hashtag)


# values_by_tweets = sorted(values, key=lambda k: k["value"]['tweets'],reverse=True) 
# print
# print "Winners : most tweets"
# for hashtag in values_by_tweets[0:10]:
#     print_hasthag(hashtag)

print
print " done in %fs" % (time() - t0)
# print "%d dates and"%len(dates),
print " %d values returned"%len(values)

