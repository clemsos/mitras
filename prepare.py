#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This file contains the process of extracting all entities from tweets
Input : csv file
Output : mongo db
'''

from models.tweet import Tweet # Connect to mongo
import lib.tweetminer as minetweet
from lib.nlp import NLPMiner
from minimongo import configure
import timeit
import csv
from pprint import pprint
import bson

# SETTINGS
nbRecords=str(500)
# csv_file="data/sampleweibo.csv"
csv_file="/home/clemsos/Data/HKU/weiboscope/week1.csv"


# LOGGING
tweets_count=0
mentions_count=0
urls_count=0
hashtags_count=0
tags_count=0
unvalid_tweets=0

# measure time
start = timeit.default_timer()


def progress_bar(progress):
    print '\r[{0}] {1}'.format('#'*(progress/10), progress)

# PROCESS all tweets in csv file
nlp=NLPMiner()

i=1 # iteroator to remember row number on csv
with open(csv_file, 'r') as f:

    print 'processing data...'
    next(f) # skip csv header
    data = csv.reader(f)

    # one row at a time
    for row in data: 

        # show progress bar (slow down the process enormously)
        # progress_bar(tweets_count)

        # create Tweet object
        t=Tweet(row)

        # Extract tweet entities
        mentions,urls,hashtags,clean=minetweet.extract_tweet_entities(t.txt)
        
        # add to Tweet
        t.mentions=mentions
        t.urls=urls
        t.hashtags=hashtags
        clean=clean # text-only version of the tweet for NLP

        # Extract keywords
        dico=nlp.extract_dictionary(clean)

        # remove stopwords and store clean dico
        t.dico=nlp.remove_stopwords(dico)

        # extract entities
        # TODO : ignore stopwords
        t.entities=nlp.extract_named_entities_from_dico(t.dico)
        
        # Some count for stats
        mentions_count+=len(mentions)
        urls_count+=len(urls)
        hashtags_count+=len(hashtags)
        tags_count+=len(t.entities)

        t.row=i

        valid_utf8 = True
        try:
            t.txt.decode('utf-8')
        except UnicodeDecodeError:
            unvalid_tweets+=1
            valid_utf8 = False
            print 'Tweet not utf-8 compatible'
            pprint(t)
        

        if valid_utf8 is True:
            try:
                t.save()
                tweets_count+=1
            except bson.errors.InvalidStringData:
                print 'URL not utf-8 compatible'
                pprint(t)


        

stop = timeit.default_timer()
elapsed=stop-start
print str(elapsed)+"s"

# LOG

print "-"*10
print "mentions_count            : "+str(mentions_count)
print "urls_count                : "+str(urls_count)
print "hashtags_count            : "+str(hashtags_count)
print "unvalid tweets            : "+str(unvalid_tweets)
print "TOTAL tweet entities      : "+str(mentions_count+urls_count+hashtags_count)
print "TOTAL named entities (NER): "+str(tags_count)

print "-"*10
print "TOTAL tweets processed    : "+str(tweets_count)
print "in                        : "+str(elapsed)+" s"