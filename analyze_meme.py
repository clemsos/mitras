#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, csv, json
from time import time 
import datetime
from collections import Counter
import lib.tweetminer as minetweet
from lib.users import UserAPI
import networkx as nx
import community
from lib.nlp import NLPMiner
import locale
from lib.mongo import MongoDB

results_path="/home/clemsos/Dev/mitras/results/"
meme_names=["biaoge"]
# meme_names=[ meme for meme in os.listdir(results_path) if meme[-3:] != "csv"]
# meme_names=[
#  'biaoge',
#  'thevoice',
#  'moyan',
#  'hougong',
#  'gangnam',
#  'sextape',
#  'dufu',
#  'ccp',
#  'yuanfang',
#  'qiegao']


print meme_names


t0=time()
minetweet.init_tweet_regex()


locale.setlocale(locale.LC_ALL, "")

nlp=NLPMiner()

stoplist=[i.strip() for i in open("lib/stopwords/zh-stopwords","r")]
stoplist+=[i.strip() for i in open("lib/stopwords/stopwords.txt","r")]
stoplist+=["转发","微博","说 ","一个","【 ","年 ","转 ","请","＂ ","问题","知道","中 ","已经","现在","说","【",'＂',"年","中","今天","应该","真的","月","希望","想","日","这是","太","转","支持"]
# stoplist+=["事儿","中国"]


api=UserAPI()
words_users_time=[]

def get_province(_userid):
    province_code= api.get_province(_userid)
    # print province_code
    try :
        return api.provinces[province_code]
    except KeyError :
        return 0
        pass

for meme_name in meme_names:

    # Init
    # tstart=time()
    print "Processing meme '%s'"%meme_name

    # files names
    meme_path=outfile=results_path+meme_name
    meme_csv=meme_path+"/"+meme_name+".csv"

    jsondata={}
    jsondata["meme_name"]=meme_name

    users=[]
    users_edges=[]

    words=[]
    words_users=[]
    words_edges={}

    count=0

    #  words_time={}
    # user_edges_time=[]
    # words_users_time={}

    by_time={}
    print "processing tweets..."
    # process the data
    with open(meme_csv, 'rb') as csvfile:
        memecsv=csv.reader(csvfile)
        memecsv.next() # skip headers

        for row in memecsv:
            # extract text
            t=row[1]    
            count+=1
            
            # time (round and store)
            d=datetime.datetime.strptime(row[9], "%Y-%m-%dT%H:%M:%S")
            day = datetime.datetime(d.year,d.month,d.day,d.hour,0,0)
            timestamp=day.strftime("%s")
            
            # regexp extract tweet entities
            mentions,urls,hashtags,clean=minetweet.extract_tweet_entities(t)
                      
            # User diffusion graph
            user_diff=[]
            users_to_users=[]
            for mention in mentions:
                users_to_users.append((row[0],mention))
                # user_edges_time.append((row[0],mention,timestamp))
                if mention not in user_diff : user_diff.append(mention)

                # retweeted_uid
            if row[7] != "" : 
                users_to_users.append((row[7],row[0]))
                # user_edges_time.append((row[7],row[0],timestamp))
                if row[7] not in user_diff : user_diff.append(row[7])
            
            users_edges+=users_to_users # store all interactions
            users+=user_diff # store all users
            
            # extract text 
            dico=nlp.extract_dictionary(clean)

            # remove stopwords and get clean dico
            clean_dico=nlp.remove_stopwords(dico)
            
            # remove more stopwords
            tmp_words=[w for w in clean_dico if w.encode('utf-8') not in stoplist and w[0] != "u" ]
            words+=tmp_words # global list for counter  
            
            # words edges
            words_to_words=[]
            words_to_users=[]
            for w in tmp_words :
                
                # word edges
                words_to_words+=[(w,t) for t in tmp_words if t!=w]
                
                # word to users
                words_to_users+=[(w,u) for u in user_diff]
                
                try: words_edges[w]
                except KeyError: words_edges[w]=[]
                words_edges[w]+=[(w,t) for t in tmp_words if t!=w]
            
            # words_edges+=words_to_words
            words_users+=words_to_users
            
            # store data by time
            try : by_time[timestamp]
            except KeyError: by_time[timestamp]={}
                
            # count
            try : by_time[timestamp]["count"]
            except KeyError: by_time[timestamp]["count"]=0
            by_time[timestamp]["count"]+=1
            
            # users edges
            try: by_time[timestamp]["user_edges"]
            except KeyError: by_time[timestamp]["user_edges"]=[]
            by_time[timestamp]["user_edges"]+=users_to_users
            
            # users nodes
            try: by_time[timestamp]["user_nodes"]
            except KeyError: by_time[timestamp]["user_nodes"]=[]
            by_time[timestamp]["user_nodes"]+=user_diff
            
            # words nodes
            try: by_time[timestamp]["words_nodes"]
            except KeyError: by_time[timestamp]["words_nodes"]=[]
            by_time[timestamp]["words_nodes"]+=tmp_words
            
            # word edges
            try: by_time[timestamp]["words_edges"]
            except KeyError: by_time[timestamp]["words_edges"]=[]
            by_time[timestamp]["words_edges"]+=words_to_words
            
            # word edges
            try: by_time[timestamp]["words_to_users"]
            except KeyError: by_time[timestamp]["words_to_users"]=[]
            by_time[timestamp]["words_to_users"]+=words_to_users

    print "processing done"


    # parse provinces for all users
    user_provinces={}
    unique_users=[u[0] for u in Counter(users).most_common()]
    for user in unique_users:
        province=get_province(user)
        user_provinces[user]=province

    # User graph info
    print "USER GRAPH"
    print "-"*20
    print "Edges (total number) : %d edges"%len(users_edges)

    # remove users edges that have a minium value of minimum_exchange
    graphsize=[c[1] for c in Counter(users_edges).most_common()]
    occurences=Counter(graphsize).most_common()
    # print occurences
    minimum_exchange=1

    # create graph object
    edges_weighted=[str(p[0][0]+" "+p[0][1]+" "+str(p[1])) for p in Counter(users_edges).most_common() if p[1] > minimum_exchange]
    print "Weighted edges %d"%len(edges_weighted)

    G = nx.read_weighted_edgelist(edges_weighted, nodetype=str, delimiter=" ",create_using=nx.DiGraph())

    # dimensions
    N,K = G.order(), G.size()
    print "Nodes: ", N
    print "Edges: ", K

    allowed_users=G.nodes()

    # Average degree
    avg_deg = float(K)/N
    print "Average degree: ", avg_deg

    # Average clustering coefficient
    ccs = nx.clustering(G.to_undirected())
    avg_clust_coef = sum(ccs.values()) / len(ccs) 
    print "Average clustering coeficient: %f"%avg_clust_coef
        
    # Communities
    user_communities = community.best_partition(G.to_undirected()) 
    modularity=community.modularity(user_communities,G.to_undirected())
    print "Modularity of the best partition: %f"%modularity
    print "Number of partitions : ", len(set(user_communities.values()))

    # betweeness_centrality
    print "computing betweeness_centrality... (this may take some time)"
    users_btw_cent=nx.betweenness_centrality (G.to_undirected())
    print "computing done"

    # WORD graph info
    print "WORD GRAPH"
    print "-"*20
    print "%d words edges"%len(words_edges)

    words_edges_weighted=[]
    words_minimum_exchange=200
    top_words_limit=500

    words_allowed=[]
    c in Counter(words).most_common(top_words_limit):
        try: 
            int(c[0])
            words_allowed.append(c[0])
        except ValueError:
            pass
            
    print "%d words_allowed"%len(words_allowed)

    for word in words_edges:
        if word in words_allowed:
            targets=[(c[0][1],c[1]) 
                     for c in Counter(words_edges[word]).most_common() 
                     if  c[0][0] in words_allowed
                     and c[0][1] in words_allowed
                     and  c[1]>words_minimum_exchange
                     ]    
            words_edges_weighted+=[(word,w[0],w[1]) for w in targets]
        
    print "Words weighted edges %d"%len(words_edges_weighted)

    wordIndex={}
    for i,w in enumerate(words_allowed): wordIndex[w]=i;

    words_edges_weightedlist=[str(wordIndex[w[0]])+" "+str(wordIndex[w[1]])+" "+str(w[2]) for w in words_edges_weighted]    
    # print words_edges_weightedlist

    Gw = nx.read_weighted_edgelist(words_edges_weightedlist, nodetype=str, delimiter=" ",create_using=nx.DiGraph())

    # dimensions
    Nw,Kw = Gw.order(), Gw.size()
    print "Nodes: ", Nw
    print "Edges: ", Kw

    # Average degree
    words_avg_deg = float(Kw)/Nw
    print "Average degree: ", words_avg_deg

    # Average clustering coefficient
    ccsw = nx.clustering(Gw.to_undirected())
    words_avg_clust_coef = sum(ccsw.values()) / len(ccsw) 
    print "Average clustering coeficient: %f"%words_avg_clust_coef
        
    # Communities
    words_communities = community.best_partition(Gw.to_undirected()) 
    words_modularity=community.modularity(words_communities,Gw.to_undirected())
    print "Modularity of the best partition: %f"%words_modularity
    print "Number of partitions : ", len(set(words_communities.values()))

    # betweeness_centrality
    print "computing betweeness_centrality... (this may take some time)"
    words_btw_cent=nx.betweenness_centrality (Gw.to_undirected())
    print "computing done"

    # parse data using time reference

    timeframes=[]
    word_median=5
    word_edge_median=25
    multi_median=15

    for _time in by_time:
    #    if(time=="1346572800"): break # single row for test 
        
        print 
        print _time, "-"*20
        
        tf=by_time[_time]
        timeframe={}
        
        # get user graph
        timeframe["user_nodes"]=[{
                                  "name":u[0],
                                  "count":u[1], 
                                  "province":user_provinces[u[0]], 
                                  "community":user_communities[u[0]],
                                  "btw_cent":users_btw_cent[u[0]]} 
                                 for u in Counter(tf["user_nodes"]).most_common() 
                                 if u[0] in allowed_users]
        
        print "%d users"%len(timeframe["user_nodes"])
        
        timeframe["user_edges"]=[{
                                  "source":u[0][0],
                                  "target":u[0][1],
                                  "weight":u[1]
                                  } 
                                  for u in Counter(tf["user_edges"]).most_common()
                                  if u[0][0] in allowed_users and u[0][1] in allowed_users]
        
        print "%d users edges"%len(timeframe["user_edges"])
        
        timeframe["provinces_edges"]=[]
        for u in timeframe["user_edges"]:
            try : source=user_provinces[u["source"]]
            except KeyError: pass
            try : target=user_provinces[u["target"]]
            except KeyError: pass    
            if source and target : timeframe["provinces_edges"].append({"source":source,"target":target, "weight":u["weight"]})
        
        print "%d provinces edges"%len(timeframe["provinces_edges"])
        
        timeframe["words_nodes"]=[{
                                    "name":w[0],
                                    "count":w[1]
                                    # "btw_cent":words_btw_cent[str(wordIndex[w[0]])],
                                    # "community":words_communities[str(wordIndex[w[0]])]
                                  } 
                                  for w in Counter(tf["words_nodes"]).most_common()
                                  if w[0] in words_allowed
                                  if w[1]>word_median]
        
        print "%d words"%len(timeframe["words_nodes"])
        
        words_edges_allowed= [w
                              for w in tf["words_edges"] 
                              if w[0]!=w[1]  
                              and w[0] in words_allowed
                              and w[1] in words_allowed
                              ]
                        
        # timeframe["words_edges"]=[{"source":w[0][0],"target":w[0][1],"weight":w[1]} for w in Counter(words_edges_allowed).most_common()]
        # print "%d words edges"%len(timeframe["words_edges"])
        
        
        words_edges_undirected=[]
        for we in words_edges_allowed:
            a=[we[0],we[1]]
            a.sort()
            words_edges_undirected.append(tuple(a))

        
        timeframe["words_edges"]=[{ "source":w[0][0],
                                               "target":w[0][1],
                                               "weight":w[1]}
                                                for w in  Counter(words_edges_undirected).most_common()
                                                if w[1]>word_edge_median]
        
        print "%d words_edges"%len(timeframe["words_edges"])
        
        timeframe["multi_graph"]=[{"word":w[0][0],
                       "user":w[0][1],
                       "weight":w[1]} 
                        for w in Counter(tf["words_to_users"]).most_common()
                        if w[0][1] in allowed_users 
                        and w[0][0] in words_allowed
                        and w[1]>multi_median
                        ]
        print "%d multilayer interactions"%len(timeframe["multi_graph"])
        
        # add province info
        for edge in timeframe["multi_graph"]:
            # print edge["user"]
            try : province=user_provinces[edge["user"]]
            except KeyError: province=""
            edge["province"]=province

        timeframes.append({"time":_time, "data":timeframe, "count":tf["count"]})

    timeframes_file=meme_path+"/"+meme_name+"_timeframes.json"

    with open(timeframes_file, 'w') as outfile:
        json.dump(timeframes, outfile)
        print "json data have been saved to %s"%(timeframes_file)


    # Variables
    collection="memes"

    # Connect to Mongo
    db=MongoDB("weibodata").db
    # count = db[collection].count()

    meme={"name":meme_name,"data":timeframes}
    db[collection].insert(meme)
        
        
