#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
from time import time 

import lib.tweetminer as minetweet
from lib.memes import list_to_csv
from lib.visualizer import create_bar_graph
import datetime

meme_name="The_Voice"

# Init
tstart=time()
minetweet.init_tweet_regex()

# name files
meme_csv=meme_name+".csv"
gephi_nodes_path=meme_name+"_nodes.csv"
gephi_edges_path=meme_name+"_edges.csv"
words_file=meme_name+"_words.csv"


generate_user_graph=True
generate_timeseries=True
generate_words=False
# ['uid', 'text', 'image', 'deleted_last_seen', 'mid', 'source', 'permission_denied', 'retweeted_uid', 'geo', 'created_at', 'retweeted_status_mid']

if generate_words: 
    from lib.nlp import NLPMiner
    nlp=NLPMiner()


with open(meme_csv, 'rb') as csvfile:
    memecsv=csv.reader(csvfile)
    memecsv.next() # skip headers
    
    edges=[]
    nodes=[]
    words=[]
    meme_urls=[]
    meme_hashtags=[]
    dates=[]
    values={}

    for row in memecsv:

         # extract text
        t=row[1]    
        
        # regexp extract tweet entities
        mentions,urls,hashtags,clean=minetweet.extract_tweet_entities(t)
        
        meme_hashtags+=hashtags
        meme_urls+=urls

        # Data : graph user diffusion
        if generate_user_graph : 
            
            d=datetime.datetime.strptime(row[9], "%Y-%m-%dT%H:%M:%S")
            timestamp=datetime.datetime(d.year,d.month,d.day,d.hour,d.minute,d.second)
            
            # if row[0] not in nodes : nodes.append(row[0])
            for mention in mentions:
                edges.append((row[0],mention,timestamp))
                # if mention not in nodes : nodes.append(mention)

            # retweeted_uid
            if row[7] != "" : 
                edges.append((row[7],row[0],timestamp))        
                # if row[7] not in nodes : nodes.append(row[7])

        # Extract keywords
        if generate_words : 
            dico=nlp.extract_dictionary(clean)
            # remove stopwords and store clean dico
            clean_dico=nlp.remove_stopwords(dico)
            words+=dico

        # collect time series data
        if generate_timeseries :
            d=datetime.datetime.strptime(row[9], "%Y-%m-%dT%H:%M:%S")
            day = datetime.datetime(d.year,d.month,d.day,0,0,0)
            i=day.strftime("%s")
            if day not in dates : # collect values 
                values[i]=0    
            values[i]+=1
            dates.append(day)

# print values

if generate_user_graph : 
    print "User diffusion : %d nodes, %d edges"%(len(nodes), len(edges))
    list_to_csv(["Id", "Label"],nodes,gephi_nodes_path)
    list_to_csv(["Source","Target", "Time"],edges,gephi_edges_path)


# create time series grpah
if generate_timeseries :
    graph_title="_time_series"
    vy=[values[v] for v in values]
    vx=[datetime.datetime.fromtimestamp(float(v)) for v in values.keys()]
    print vx,vy
    create_bar_graph(vx,vy,graph_title,True)


print  "Content : %d words, %d hashtags, %d urls"%(len(words),len(meme_urls), len(meme_hashtags))

print "done in %.3fs"%(time()-tstart)






    