#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, zipfile
import codecs
import pandas as pd
import lib.tweetminer as minetweet
from lib.nlp import NLPMiner
from lib.mongo import MongoDB
import csv

from time import time

root_path="/home/clemsos/Dev/mitras/"
raw_data_path=root_path+"data/datazip/"
clean_data_path=root_path+"data/clean/"
training_set=root_path+"data/train/trainset.csv"
train_path=root_path+"data/train/"

chunksize=1000

# init
needs_header=True
t0=time()
nlp=NLPMiner()
init_files=[True,True,True,True]

# Connect to Mongo
db=MongoDB("weiboclean").db

# where the raw data is
collection="training"

# get corpus length
tweets_count=db[collection].count()
print str(tweets_count)+" tweets in the db"
print 10*"-"


stop_hashtags=["晚安","搞笑","应用广场签到","","微盘签到", None]

# clean training set
with open(training_set, 'w') as train:
    train.write("")

# loop through each csv
for path, subdirs, files in os.walk(raw_data_path):
    
    for filename in files:
        
        # open file store for training set
        with open(training_set, 'a') as train:
            
            if filename[-3:] == "zip" and filename[:4] == "week": # get only zip files 
                zip_path=path+filename
                raw_csvname=filename.split(".")[0]+".csv" 
                clean_csvname=clean_data_path+filename.split(".")[0]+".csv" 
                
                with zipfile.ZipFile(zip_path) as z: # open zip
                    f = z.open(raw_csvname) # read csv
                    csvfile=pd.read_csv(f, iterator=True, chunksize=chunksize) # parse csv with pandas
                    print "#"*20

                    # init training set
                    hashtrain = []
                
                    # reset clean data content
                    with open(clean_csvname, 'w') as toclean:
                        toclean.write("")

                    # create clean data
                    with open(clean_csvname, "a") as clean_csv:
                        
                        clean_needs_header=True

                        # read csv chunk by chunk
                        for i,df in enumerate(csvfile): 

                            if i==1 : break
                            print i
                            
                            # extract tweet entities
                            mentions,urls,hashtags,clean=[],[],[],[]

                            for j,t in enumerate(df.text.values):
                                try : # prevent empty value to break thread
                                    m,u,h,c=minetweet.extract_tweet_entities(t)
                                except TypeError:
                                    m,u,h,c=[],[],[],[]

                                # compute diffusion
                                diff=m
                                if df.retweeted_uid[j] != "" : diff.append(df.uid[j])

                                # define fixed size for arrays (data frame)
                                len_m=15
                                len_u= 5
                                len_h= 3

                                # fill arrays with zeros to have constant size
                                m = m + [None]*(len_m - len(m))
                                u = u + [None]*(len_u - len(u))
                                h = h + [None]*(len_h - len(h))

                                mentions.append(m[0:len_m])
                                urls.append(u[0:len_u]),hashtags.append(h[0:len_h])

                                # Extract keywords
                                dico=nlp.extract_dictionary(c)
                                # remove stopwords and store clean dico
                                clean_dico=nlp.remove_stopwords(dico)

                                clean.append(clean_dico)

                                clean_utf=[c.encode("utf-8") for c in clean_dico]
                                # append all hashtags to training set
                                # remove most common hashtags
                                for hstg in h:
                                    if hstg not in stop_hashtags :
                                        hashtrain.append((hstg,df.mid[j], m, df.uid[j], diff ,df.created_at[j],clean_utf))
                                     
                            # convert raw data to clean data frame
                            df_mentions=pd.DataFrame(mentions)
                            df_mentions.shape
                            df_mentions.columns=["mention_"+str(x) for x in range(0,len_m)]
                            df_mentions["mid"]=df["mid"]

                            df_hashtags=pd.DataFrame(hashtags)
                            df_hashtags.columns=["hashtag"+str(x) for x in range(0,len_h)]
                            df_hashtags["mid"]=df["mid"]

                            df_urls=pd.DataFrame(urls)
                            df_urls.columns=["url"+str(x) for x in range(0,len_u)]
                            df_urls["mid"]=df["mid"]

                            df=pd.merge(df,df_mentions)
                            df=pd.merge(df,df_hashtags)
                            df=pd.merge(df,df_urls)
                            
                            df["dico"]=clean
                            
                            #save clean data
                            df.to_csv(clean_csv, mode='a', index=False, sep=";", header=clean_needs_header)
                            clean_needs_header=False
                        
                        df_train=pd.DataFrame(hashtrain)
                        df_train.columns=["hashtag","mid", "mentions", "users", "diffusion", "created_at","phrase"]

                        # df_train.to_csv(train, mode='a', index=False,header=needs_header,sep=";")
                        # df_train.to_json(train, mode='a')
                        # db[collection].insert(df_train.to_json())

                        grouped=df_train.groupby("hashtag", sort=True).agg(lambda x: x.tolist())
                        
                        def flatten(arr):
                            return [item for sublist in arr for item in sublist]

                        txt=flatten(grouped.phrase)
                        tweets=flatten(grouped.mid)
                        users=flatten(grouped.users)
                        tmp_diff=flatten(grouped.diffusion)
                        diffusion=flatten(tmp_diff)

                        

                        types=[(txt,"txt"),(diffusion,"diffusion"),(tweets,"tweets"),(users,"users")]

                        for ii,mytype in enumerate(types):

                            proto_filename=train_path+"train."+mytype[1]
                            # print proto_filename

                            # if not os.path.exists(proto_filename):
                            # t0=time()        
                            # init file

                            if init_files[ii] is True:
                                with open(proto_filename, "w") as proto_file:
                                    proto_file.write("")
                                    init_files[ii]=False



                            print " creating raw corpus : %s"%proto_filename
                            with open(proto_filename, "a") as proto_file:
                                # print mytype[0]
                                csv.writer(proto_file).writerow(mytype[0])
                                
                            # else:
                            #     print " Raw corpus already exists %s "%proto_filename
                            #     print 

                        needs_header=False # add header on the first line

print "Raw files processed"
print "done in %.3fs"%(time()-t0)

