#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.plot import create_bar_graph
from lib.mongo import MongoDB
from lib.stats import get_tweets_volume_time_series, get_tweet_volume_per_user

from collections import Counter

collection="week1"

# Connect to Mongo
db=MongoDB("weibodata").db
data=db[collection]
tweets_count=data.count()
print 10*"-"
print "%s tweets in the db"%tweets_count

# Load data

# Visualize tweets volume by day
# dates,values=get_tweets_count_time_series(data, 10)
# title ='Volume of tweets in '+collection+' by day'
# create_bar_graph(dates,values,title, False)

tweet_per_user=get_tweet_volume_per_user(data, 10000)
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