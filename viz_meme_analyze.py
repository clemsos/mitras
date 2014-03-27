#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
from time import time 
import datetime
from collections import Counter
import lib.tweetminer as minetweet
from lib.memes import list_to_csv
from lib.visualizer import create_bar_graph
import json


meme_name="thevoice"

# Init
tstart=time()
minetweet.init_tweet_regex()

# d3
generate_users_map=True
generate_d3_graph=True
generate_timeseries=True
generate_words=True

# gephi
generate_gephi_graph=False

# name files
meme_path=outfile="/home/clemsos/Dev/mitras/results/"+meme_name
meme_csv=meme_path+"/"+meme_name+".csv"

timeseries_file=meme_path+"/"+meme_name+"_time_series.json"
d3_edges_path=meme_path+"/"+meme_name+"_d3graph.csv"
user_map_file=meme_path+"/"+meme_name+"_usermap.json"

words_file=meme_path+"/"+meme_name+"_words.json"

gephi_nodes_path=meme_path+"/"+meme_name+"_nodes.csv"
gephi_edges_path=meme_path+"/"+meme_name+"_edges.csv"


if generate_words: 
    from lib.nlp import NLPMiner
    nlp=NLPMiner()

    stoplist=[i.strip() for i in open("lib/stopwords/zh-stopwords","r")]
    stoplist+=[i.strip() for i in open("lib/stopwords/stopwords.txt","r")]
    stoplist+=["转发","微博","说 ","一个","【 ","年 ","转 ","请","＂ ","问题","知道","中 ","已经","现在","说","【",'＂',"年","中","今天","应该","真的","月","希望","想","日","这是","太","转","支持"]


if generate_users_map:
    # get user data 
    from lib.users import UserAPI
    api=UserAPI()

    def get_province(_userid):
        province_code= api.get_province(_userid)
        # print province_code
        try :
            return user_provinces.append(api.provinces[province_code])
        except KeyError :
            print "error"
            pass

# ['uid', 'text', 'image', 'deleted_last_seen', 'mid', 'source', 'permission_denied', 'retweeted_uid', 'geo', 'created_at', 'retweeted_status_mid']
# process the data
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
    user_provinces=[]

    for row in memecsv:

        # extract text
        t=row[1]    
        
        # regexp extract tweet entities
        mentions,urls,hashtags,clean=minetweet.extract_tweet_entities(t)
        
        meme_hashtags+=hashtags
        meme_urls+=urls

        # Data : graph user diffusion
        if generate_gephi_graph or generate_d3_graph : 
            
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
            
            # add words not in stopwords
            words+=[w for w in clean_dico if w.encode('utf-8') not in stoplist]


        # Collect time series data
        if generate_timeseries :
            d=datetime.datetime.strptime(row[9], "%Y-%m-%dT%H:%M:%S")
            day = datetime.datetime(d.year,d.month,d.day,d.hour,0,0)
            i=day.strftime("%s")
            if day not in dates : # collect values 
                values[i]=0    
            values[i]+=1
            dates.append(day)

        # collect province for all users
        if generate_users_map :
            user_provinces.append(get_province(row[0]))
            
            # for mention in mentions:
            #     user_provinces.append(get_province(mention))

            # # retweeted_uid
            # if row[7] != "" : 
            #     user_provinces.append(get_province(row[7]))
            

if generate_gephi_graph : 
    print "User diffusion : %d nodes, %d edges"%(len(nodes), len(edges))
    list_to_csv(["Id", "Label"],nodes,gephi_nodes_path)
    list_to_csv(["Source","Target", "Time"],edges,gephi_edges_path)

if generate_d3_graph :
    print "User diffusion : %d nodes, %d edges"%(len(nodes), len(edges))
    user_graph=[(e[0], e[1]) for e in edges]
    user_graph_weighted=[[p[0][0],p[0][1],p[1]] for p in Counter(user_graph).most_common()  if p[1] > 2]
    list_to_csv(["source","target","weight"],user_graph_weighted,d3_edges_path)

# create time series grpah
if generate_timeseries :
    graph_title="_time_series"
    with open(timeseries_file, 'w') as outfile:
        json.dump([{"timestamp" : v, "count": values[v]  } for v in values], outfile)
    print "json data have been saved to %s"%(timeseries_file)

    # vy=[values[v] for v in values]
    # vx=[datetime.datetime.fromtimestamp(float(v)) for v in values.keys()]
    # print vx,vy
    # create_bar_graph(vx,vy,graph_title,True)

if generate_users_map:
    map_data={}
    map_data["title"]="Population distribution for Sina Weibo users."
    map_data["desc"]="Based on Sina Weibo user profiles info. Data from HKU Weiboscope."
    map_data["credits"]="by Clement Renaud - 2013"
    map_data["units"]="Volume of tweets (per 100)"
    map_data["provinces"]=[{ "name": p[0], "count" :(p[1]/100) } for p in Counter(user_provinces).most_common()]
    with open(user_map_file, 'w') as outfile:
        json.dump(map_data, outfile)
    print "json data have been saved to %s"%(user_map_file)

if generate_words:    

    data_words={}
    data_words["urls"]=[ {"name":url[0],"count":url[1]} for url in Counter(meme_urls).most_common() if url[1]>10 ]

    data_words["hashtags"]=[{"name":hashtag[0],"count":hashtag[1]} for hashtag in Counter(meme_hashtags).most_common() if hashtag[1]>10]

    data_words["words"]=[{"name":word[0],"count":word[1]} for word in Counter(words).most_common() if word[1]>10]

    data_words["urls_count"]=len(meme_urls)
    data_words["hashtags_count"]=len(meme_hashtags)

    with open(words_file, 'w') as outfile:
        json.dump(data_words, outfile)
    print "json data have been saved to %s"%(words_file)
    
    



print  "Content : %d words, %d hashtags, %d urls"%(len(words),len(meme_urls), len(meme_hashtags))

print "done in %.3fs"%(time()-tstart)

