results_path="/home/clemsos/Dev/mitras/results/"

import os, csv, json
from time import time 
import datetime
from collections import Counter
import lib.tweetminer as minetweet
import elasticsearch

es = elasticsearch.Elasticsearch(["localhost:9200"])

meme_name="biaoge"


# Init
t0=time()
print "Processing meme '%s'"%meme_name

# files names
meme_path=outfile=results_path+meme_name
meme_csv=meme_path+"/"+meme_name+".csv"

##### search rt ids

# mids=[]
# rt_mids=[]
# c=0
# with open(meme_csv, 'rb') as csvfile:
#     memecsv=csv.reader(csvfile)
#     memecsv.next() # skip headers

#     for i,row in enumerate(memecsv):
#         # if i==0: print row[4] 
        
#         # extract text
#         t=row[1]

#         # add rt
#         mids.append(row[4])
#         if(row[len(row)-1] != ""): rt_mids.append(row[len(row)-1])

#         # regexp extract tweet entities
#         # mentions,urls,hashtags,clean=minetweet.extract_tweet_entities(t)

# mids_to_fetch=[ mid for mid in rt_mids if mid not in mids]
# print i

mids_to_fetch=['mcXmqcsUFU', 'mcXmqcsUFU', 'mT5C3W0M3g', 'mT5C3W0M3g', 'mT5C3W0M3g', 'mPop6jgvMK', 'mFLqdUnmw8']

print "%d messages to fetch"%len(mids_to_fetch)



# ES : Build query
mids_query=""
for i,k in enumerate(mids_to_fetch):
    mids_query+='\"'+k+'\"'
    if i+1 < len(mids_to_fetch): mids_query+= " OR "

print mids_query

query={ "query": {
        "query_string": {
            "query": mids_query
         }
      }
    }

query= {
    "bool": {
        "must": [
            {
                "match_all": { }
            },
            {
                "term": {
                    "tweet.mid": mids_query
                }
            }
        ]
    
    }
}


index_name="weiboscope_34_35"

res = es.search(index=index_name, body=query)

data_size=res['hits']['total']

print "Total %d Hits from %s" % (data_size, index_name)

print "Everything done in %.3fs"%(time()-t0)