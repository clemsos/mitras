#!/usr/bin/env python
# -*- coding: utf-8 -*-


from time import time
import os, zipfile
import codecs
import pandas as pd
import numpy as np
import lib.tweetminer as minetweet
from lib.nlp import NLPMiner
from lib.mongo import MongoDB

root_path="/home/clemsos/Dev/mitras/"
raw_data_path=root_path+"data/datazip/"

# sample_scale=4 #number of iterations
chunksize=5000

# init
t0=time()
# nlp=NLPMiner()

# Connect to Mongo
db=MongoDB("weiboclean").db
collection=db["tweets_with_hastags"]

# get corpus length
tweets_count=collection.count()
print str(tweets_count)+" tweets in the db"
print 10*"-"

# add of stop-hahstags t remove most common occurence
stop_hashtags_file=root_path+"/lib/stopwords/stop_hashtags"
stop_hashtags=[i.strip() for i in open(stop_hashtags_file)]

###
# COLLECT DATA FOR HASHTAGS
###

collection.drop()
collection.ensure_index("hashtags")
collection.ensure_index("created_at")
collection.ensure_index("urls")
collection.ensure_index("uid")
collection.ensure_index("mentions")
collection.ensure_index("geo")
# collection.ensure_index("retweeted_status_mid")
# collection.ensure_index("retweeted_status_uid")

# all tweets containing hashtags into mongo
for path, subdirs, files in os.walk(raw_data_path):
    
    # loop through each files
    for i_file, filename in enumerate(files): 
        # if i==1 : break
        # read zipped csv files
        if filename[-3:] == "zip" and filename[:4] == "week": # get only zip files 

            zip_path=path+filename
            raw_csvname=filename.split(".")[0]+".csv" 
            # clean_csvname=clean_data_path+filename.split(".")[0]+".csv" 
            
            with zipfile.ZipFile(zip_path) as z: # open zip
                f = z.open(raw_csvname) # read csv
                csvfile=pd.read_csv(f, iterator=True, chunksize=chunksize) # parse csv with pandas
                print raw_csvname+"#"*20

                # init training set
                hashtrain = []
            
                # create clean data
                tstart=time()
                clean_needs_header=True

                # read csv chunk by chunk
                for i,df in enumerate(csvfile): 
                    # if i==1 : break
                    print i
                    
                    # extract tweet entities
                    mentions,urls,hashtags,clean=[],[],[],[]

                    for j,t in enumerate(df.text.values):
                        
                        try : # prevent empty value to break thread
                            m,u,h,c=minetweet.extract_tweet_entities(t)
                        except TypeError:
                            m,u,h,c=[],[],[],[]


                        # check if there is none of the most common hashtags
                        if len([hashtag for hashtag in h if hashtag in stop_hashtags]) == 0 :

                            # compute diffusion
                            # diff=m
                            # if df.retweeted_uid[j] != "" : diff.append(df.uid[j])

                            # Extract keywords
                            # dico=nlp.extract_dictionary(c)
                            
                            # remove stopwords and store clean dico
                            # clean_dico=nlp.remove_stopwords(dico)

                            tweet_data={}
                            # add raw tweet info
                            for f in df : 
                                val=df[f][j]
                                # convert numpy instance to int
                                if isinstance(val, np.generic):
                                    val=np.asscalar(val)
                                
                                # prevent bad encoding from breaking files
                                if type(val) == str: 
                                    try :
                                        val.decode("utf-8")
                                    except UnicodeDecodeError:
                                        val=""
                                tweet_data[f] = val

                            # prevent bad encoding from breaking files
                            def unicode_safe(arr):
                                safe=[]
                                for item in arr:
                                    if type(item) is str: 
                                        try:
                                            coded_item=item.decode("utf-8")
                                        except UnicodeDecodeError:
                                            coded_item=""
                                        safe.append(coded_item)
                                    else :
                                        try :
                                            coded_item=item.encode("utf-8")
                                        except UnicodeDecodeError:
                                            coded_item=""
                                        safe.append(coded_item)
                                # print safe
                                return safe

                            # tweet_data["dico"]=unicode_safe(clean_dico)
                            tweet_data["mentions"]=unicode_safe(m)
                            tweet_data["hashtags"]=unicode_safe(h)
                            tweet_data["urls"]=unicode_safe(u)

                            # print tweet_data["hashtags"]

                            collection.insert(tweet_data)
                            # print "record added to mongo"

                print "done in %.3fs"%(time()-tstart)

print "Raw files processed"
print "done in %.3fs"%(time()-t0)
