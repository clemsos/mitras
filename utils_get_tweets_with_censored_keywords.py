#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
from lib.nlp import NLPMiner 
import lib.tweetminer as minetweet
# from lib.visualizer import create_tag_cloud
from collections import Counter

outfile="out/censored_tweets_2012-02-05_2012-04-20.tsv"

# labels="retweeted_status_mid,text,created_at,deleted_last_seen,mid,source,permission_denied,retweeted_uid,geo,image,uid".split(',')
censored_tweets=[]
with open(outfile, 'rb') as cs_file:
    csv_censor=csv.reader(cs_file)
    censored_tweets=[word for word in csv_censor]

# censored_tweets


# get keywords
nlp=NLPMiner()
minetweet.init_tweet_regex()

stoplist=[i.strip() for i in open("lib/stopwords/zh-stopwords","r")]
stoplist+=[i.strip() for i in open("lib/stopwords/stopwords.txt","r")]
stoplist+=["转发","微博","说 ","一个","【 ","年 ","转 ","请","＂ ","问题","知道","中 ","已经","现在","说","【",'＂',"年","中","今天","应该","真的","月","希望","想","日","这是","太","转","支持"]

# store all keywords
texts=[]

hashtags_censored=[]

for t in censored_tweets:
    # t=tweet["_source"]

    # Extract tweet entities
    mentions,urls,hashtags,clean=minetweet.extract_tweet_entities(t[1])

    # Extract keywords
    dico=nlp.extract_dictionary(clean)

    # remove stopwords and store clean dico
    dico=nlp.remove_stopwords(dico)

    if len(hashtags) is not 0:
        for h in hashtags:
            hashtags_censored.append(h)

    # remove stopwords 2
    keywords=[w for w in dico if w.encode('utf-8') not in stoplist]
    if len(keywords) is not 0:
        for k in keywords:
            texts.append(k)

# count occurence 
# create_tag_cloud(texts, "Censored Tweets")
top_words=Counter(texts)

print "20 Most common words"
for c in top_words.most_common(20):
    print c[0],c[1]


top_h=Counter(hashtags_censored)

print "Hastags in censored post"
for c in hashtags_censored:
    print c
