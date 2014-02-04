#!/usr/bin/env python
# -*- coding: utf-8 -*-
import elasticsearch
import csv
import unicodedata
from lib.nlp import NLPMiner 
import lib.tweetminer as minetweet
from lib.visualizer import create_tag_cloud
from collections import Counter

outfile="out/censored_tweets_2012-02-05_2012-04-20.tsv"


# init es client
es = elasticsearch.Elasticsearch(['http://localhost:9200/'])

# get column names
indices=es.indices.get_mapping(index="weiboscope",doc_type="tweet")
colnames=indices["tweet"]["properties"]

# Replace the following Query with your own Elastic Search Query
res = es.search(index="weiboscope", body=
{
  "query": {
    "filtered": {
      "query": {
        "query_string": {
            "query": "permission_denied:exists"
         }
      },
      "filter": {
        "numeric_range": {
          "created_at": {
            "gte": "2012-02-05",
            "lte": "2012-04-20"
          }
        }
      }
    }
  }
}, size=3669)  #this is the number of rows to return from the query... to get all queries, run script, see total number of hits, then set euqual to number >= total hits

print("Got %d tweets" % res['hits']['total'])

sample = res['hits']['hits']
'''
with open(outfile, 'wb') as csvfile: 

    filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    
    # create header row
    filewriter.writerow([c for c in colnames])    

    for hit in sample:   #switch sample to randomsample if you want a random subset, instead of all rows
        # print hit["_source"]
        # print
        col=[]
        for colname in colnames:
            # print colname, hit["_source"][colname]

            if colnames[colname]["type"] == 'string' and hit["_source"][colname] is not None:
                    try:
                        col.append(hit["_source"][colname].encode('utf-8'))
                    except UnicodeDecodeError:
                        pass
            else:
                try:
                   col.append(hit["_source"][colname])
                except:
                    col.append("")

        filewriter.writerow(col)

print "Tweet data saved as : %s"%outfile
'''
# get keywords
nlp=NLPMiner()
minetweet.init_tweet_regex()

stoplist=[i.strip() for i in open("lib/stopwords/zh-stopwords","r")]
stoplist+=[i.strip() for i in open("lib/stopwords/stopwords.txt","r")]
stoplist+=["转发","微博","说 ","一个","【 ","年 ","转 ","请","＂ ","问题","知道","中 ","已经","现在","说","【",'＂',"年","中","今天","应该","真的","月","希望","想","日","这是","太"]

# store all keywords
texts=[]

for tweet in sample:


    t=tweet["_source"]
    
    # Extract tweet entities
    mentions,urls,hashtags,clean=minetweet.extract_tweet_entities(t["text"])

    # Extract keywords
    dico=nlp.extract_dictionary(clean)

    # remove stopwords and store clean dico
    dico=nlp.remove_stopwords(dico)


    # remove stopwords 2
    keywords=[w for w in dico if w.encode('utf-8') not in stoplist]
    if len(keywords) is not 0:
        for k in keywords:
            texts.append(k)

# count occurence 
# create_tag_cloud(texts, "Censored Tweets")
count=Counter(texts)

print "20 Most common words"
for c in count.most_common(20):
    print c[0],c[1]

