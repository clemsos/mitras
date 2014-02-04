#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from lib.plot import create_bar_graph
from lib.mongo import MongoDB
from lib.stats import get_tweets_volume_time_series
from lib.visualizer import create_bar_graph,create_pie_chart,create_tag_cloud

from time import time,strftime,strptime
from datetime import datetime
from bson.code import Code
from collections import Counter

import pylab as plt


# Connect to Mongo
collection="memes"
memes_count = 20

db=MongoDB("weibodata").db
data=db[collection]
total_memes_count=data.count()
print 10*"-"
print "%s memes in the db"%total_memes_count
print


def find_hashtags_redundant(_memes):
    hash=[]
    print hash

    for i, meme in enumerate(_memes):
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

def get_most_common_words(_tweets,_count):
    txt = []
    for t in _tweets:
        for word in t["dico"]:
            txt.append(word)

    print "%d words in meme"%len(txt)

    counter = Counter(txt).most_common(_count)
    # tags = [(word.encode("utf-8"), count) for word,count in counter]
    return counter

def create_graph_volume_time_series(_tweets):
    time_series={}
    for tweet in _tweets:
        t=datetime.strptime(str(tweet["created_at"]), "%Y-%m-%d %H:%M:%S") # 2012-01-08 14:08:03
        # round to day + hour
        day=datetime.strptime(datetime.strftime(t, "%Y-%m-%d %H:00:00"), "%Y-%m-%d %H:%M:%S")
        try: 
            time_series[day]+=1
        except KeyError : 
            time_series[day]=0
    
    dates=time_series.keys()
    values=time_series.values()

    title ='Volume of tweets for meme  by hours'
    create_bar_graph(dates,values,title, True)

def create_pie_chart_post_per_users(_tweets):
    tweets_per_users={}
    for tweet in _tweets:
        user=tweet["userId"]
        try: 
            tweets_per_users[user]+=1
        except KeyError : 
            tweets_per_users[user]=1

    # dates=tweets_by_users.keys()
    # values=tweets_by_users.values()

    tweet_per_user_count= {}
    for user, count in tweets_per_users.items():
        try: 
            tweet_per_user_count[count]+=1
        except KeyError :
            tweet_per_user_count[count]=1

    title ='Volume of tweets in meme per users'
    # create_bar_graph(dates,values,title, True)
    h={v:k for k, v in tweet_per_user_count.items()}
    
    labels=[]
    values=[]
    total=0
    for t in sorted(h):
        labels.append("%s messages"%(h[t]))
        values.append(t)
        total+=t
        print "%s users have posted %s messages"%(t,h[t])

    print total

    percent=[v/float(total)*100 for v in values]
    print percent
    for i,l in enumerate(labels):
        print "%.2f percent of %s"%(percent[i],l)

    title="Number of post per users"
    create_pie_chart(values, labels,title, True )

# query = { "name" : "tmpgrKBtb"}
query = { "name" : "tmpioT57L"}
memes = list(data.find(query).limit(memes_count))
print len(memes)

# Visualize tweets volume by day

print
for meme in memes:

    # # create tag cloud
    # name='out/cloud_large.png'
    # tags=get_most_common_words(meme["tweets"],50)
    # print tags
    # create_tag_cloud(tags,name)

    # create_graph_volume_time_series(meme["tweets"])
    # create_pie_chart_post_per_users(meme["tweets"])

    # print len(meme["tweets"]), len(mentions_count)
    
    # get 5 most retweeted tweets
    mentions_count=sorted([(len(t["mentions"]),i) for i,t in enumerate(meme["tweets"])], reverse=True)
    for i in range(0,5):
        # print mentions_count[i]
        print "---"*10
        t = meme["tweets"][mentions_count[i][1]]
        print t["txt"].encode("utf-8")




    
    







    

    

    

