#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This file contains the process of extracting all entities from tweets
Input : csv file
Output : mongo db
'''

from time import time
import csv
import bson

from argparse import ArgumentParser # for command line
from models.tweet import Tweet # mongo data model


def extract_and_store_tweets(csvfile,nlp,minetweet):
    print
    print "Start processing %s ..."%csvfile
    print "*"*20

    start=time() # measure time

    # LOGGING
    tweets_count=0
    mentions_count=0
    urls_count=0
    hashtags_count=0
    tags_count=0
    unvalid_tweets=0


    i=1 # iteroator to remember row number on csv
    with open(csvfile, 'r') as f:

        # print 'Processing data...'
        next(f) # skip csv header
        data = csv.reader(f)

        # one row at a time
        for row in data: 

            # create Tweet object
            t=Tweet()

            # Populate Tweet
            t.mid=row[0]
            t.retweetFromPostId=row[1]
            t.userId=row[2]
            t.retweetFromUserId=row[3]
            t.source=row[4]
            t.hasImage=row[5]
            t.txt=row[6]
            t.geo=row[7]
            t.created_at=row[8]
            t.deleted_last_seen=row[9]
            t.permission_denied=row[10]

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
            # t.entities=nlp.extract_named_entities_from_dico(t.dico)
            
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
                print ' bad encoding : tweet ',t.mid
                # pprint(t)
            
            if valid_utf8 is True:
                try:
                    t.save()
                    tweets_count+=1
                except bson.errors.InvalidStringData:
                    print ' bad encoding : tweet ',t.mid
                    # pprint(t)

    # LOG
    print
    print "-"*10
    print " mentions_count            : %d "%mentions_count
    print " urls_count                : %d "%urls_count
    print " hashtags_count            : %d "%hashtags_count
    print " unvalid tweets            : %d "%unvalid_tweets
    print " TOTAL tweet entities      : %d "%(mentions_count+urls_count+hashtags_count)
    print " TOTAL named entities (NER): %d "%tags_count
    print
    print "-"*10
    print "TOTAL tweets processed    : %d"%tweets_count
    print " done in %.3fs"%(time()-start)
    print


def main():

    desc ="""
        prepare.py is a script to extract tweet entities from HKU Weiboscope corpus and store all results in MongoDB."""

    # init libraries
    import lib.tweetminer as minetweet
    from lib.nlp import NLPMiner

    # parse command line arguments
    usage="""
        prepare.py
        """

    parser = ArgumentParser(usage=usage, version=" 0.1", description=desc)
    parser.add_argument("csv_file", help="should be a csv file from Weiboscope corpus")
    args = parser.parse_args()

    # identify csv file
    # csv_file="/home/clemsos/Data/HKU/weiboscope/week1.csv"
    csv_file=args.csv_file
    
    # PROCESS all tweets in csv file
    nlp=NLPMiner()

    extract_and_store_tweets(csv_file,nlp, minetweet)

if __name__ == '__main__':
    main()