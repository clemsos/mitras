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
import os

# get meme_names
# meme_names=[ meme for meme in os.listdir(results_path) if meme[-3:] != "csv"]
results_path="/home/clemsos/Dev/mitras/results/"
meme_names=["biaoge"]
print meme_names

'''
# Data to be produced
words = [ Mot1, Mot2, Mot3 ]
users=[user1,user2]
provinces=[province1,province2]

words_weighted_edges=[( Mot1, Mot2, w), (Mot2, Mot3, w)]
words_users_weight= [(Mot1,User1,w),(Mot1,User2,w)]
user_weighted_edges=[(User1, User2),(User2, User2)]
user_provinces=[(user1, province1), (user2, province2)]
'''

# 
t0=time()
minetweet.init_tweet_regex()

# d3
generate_users_map=False
generate_d3_graph=False
generate_timeseries=False
generate_words_graph=True
general_info=False

# gephi
generate_gephi_graph=False

if generate_words_graph: 
    from lib.nlp import NLPMiner
    import locale
    locale.setlocale(locale.LC_ALL, "")

    nlp=NLPMiner()

    stoplist=[i.strip() for i in open("lib/stopwords/zh-stopwords","r")]
    stoplist+=[i.strip() for i in open("lib/stopwords/stopwords.txt","r")]
    stoplist+=["转发","微博","说 ","一个","【 ","年 ","转 ","请","＂ ","问题","知道","中 ","已经","现在","说","【",'＂',"年","中","今天","应该","真的","月","希望","想","日","这是","太","转","支持"]
    stoplist+=["事儿","中国"]

if generate_users_map:
    # get user data 
    from lib.users import UserAPI
    api=UserAPI()

    def get_province(_userid):
        province_code= api.get_province(_userid)
        # print province_code
        try :
            return api.provinces[province_code]
        except KeyError :
            return 0
            pass

def analyze_meme(meme_name):

    # Init
    tstart=time()
    print "Processing meme '%s'"%meme_name

    # files names
    meme_path=outfile=results_path+meme_name
    meme_csv=meme_path+"/"+meme_name+".csv"

    general_file=meme_path+"/"+meme_name+"_general.json"
    timeseries_file=meme_path+"/"+meme_name+"_time_series.json"
    d3_edges_path=meme_path+"/"+meme_name+"_d3graph.csv"
    user_map_file=meme_path+"/"+meme_name+"_usermap.json"
    words_file=meme_path+"/"+meme_name+"_words.json"

    gephi_nodes_path=meme_path+"/"+meme_name+"_nodes.csv"
    gephi_edges_path=meme_path+"/"+meme_name+"_edges.csv"

    
    # process the data
    with open(meme_csv, 'rb') as csvfile:
        # ['uid', 'text', 'image', 'deleted_last_seen', 'mid', 'source', 'permission_denied', 'retweeted_uid', 'geo', 'created_at', 'retweeted_status_mid']
        memecsv=csv.reader(csvfile)
        memecsv.next() # skip headers
        
        edges=[]
        nodes=[]
        
        words_series=[]
        words_list=[]

        meme_urls=[]
        meme_hashtags=[]
        dates=[]
        values={}
        user_provinces=[]
        count=0

        for row in memecsv:

            # extract text
            t=row[1]    
            count+=1

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
            if generate_words_graph : 
                dico=nlp.extract_dictionary(clean)
                # remove stopwords and store clean dico
                clean_dico=nlp.remove_stopwords(dico)
                
                # add words not in stopwords
                tmp_words=[w for w in clean_dico if w.encode('utf-8') not in stoplist or w[0] != "u"]
                words_series.append(tmp_words)
                words_list+=tmp_words # global list for counter

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
                province=get_province(row[0])
                if province!=0 : user_provinces.append(province)
                
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

    if general_info: 
        data_info={}
        data_info["tweets_count"]=count
        data_info["urls"]=[ {"name":url[0],"count":url[1]} for url in Counter(meme_urls).most_common() if url[1]>10 ]

        data_info["hashtags"]=[{"name":hashtag[0],"count":hashtag[1]} for hashtag in Counter(meme_hashtags).most_common() if hashtag[1]>10]

        data_info["urls_count"]=len(meme_urls)
        data_info["hashtags_count"]=len(meme_hashtags)

        with open(general_file, 'w') as outfile:
            json.dump(general_file, outfile)
        print "json data have been saved to %s"%(general_file)

        print  "Content : %d tweets %d words, %d hashtags, %d urls"%(count, len(words),len(meme_urls), len(meme_hashtags))


    if generate_words_graph: 

        data_words={}
        data_words["edges"]=[]
        # node_words=[{"name":word[0],"count":word[1]} for word in Counter(words).most_common() if word[1]>10]

        # build nodesnode_words
        node_words=[c[0] for c in Counter(words_list).most_common(500)]
        
        # print len(node_words), " nodes in words"
        tmp_words_edges=[]
        word_edges=[]

        for serie in words_series:     
            tmp_words_edges+= [(word, serie) for word in serie if word in node_words]

        for edge_pack in tmp_words_edges:
            for word in edge_pack[1]:
                if word is not edge_pack[0] and edge_pack[0] != word:
                    tmp=[edge_pack[0], word]
                    tmp.sort(cmp=locale.strcoll) # sort chinese characters to create undirected graph
                    word_edges.append((tmp[0],tmp[1]))
        
        data_words["edges"]= [ {"source" : c[0][0], "target" : c[0][1], "weight": c[1] } for c in Counter(word_edges).most_common(200) ]
    
        words_map={}
        for c in Counter(words_list).most_common():
            words_map[c[0]]=c[1]
            
        unique_nodes=[]
        for e in data_words["edges"]:
            if e["source"] not in unique_nodes : unique_nodes.append(e["source"]) 
            if e["target"] not in unique_nodes : unique_nodes.append(e["target"]) 


        data_words["nodes"]=[{"name" : node, "count": words_map[node]} for node in unique_nodes]
    

    # node_words=[{"name":word[0],"count":word[1]} for word in Counter(words).most_common() if word[1]>10]

        with open(words_file, 'w') as outfile:
            json.dump(data_words, outfile)
        print "json data have been saved to %s"%(words_file)

    print "done in %.3fs"%(time()-tstart)

for meme in meme_names:
    analyze_meme(meme)

print "Everything done in %.3fs"%(time()-t0)