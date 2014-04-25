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

def analyze_meme(meme_name):

    # Init
    tstart=time()
    print "Processing meme '%s'"%meme_name

    # files names
    meme_path=outfile=results_path+meme_name
    meme_csv=meme_path+"/"+meme_name+".csv"

    jsondata={}
    jsondata["meme_name"]=meme_name

    user_edges=[]
    user_nodes=[]
    words_series=[]
    words_list=[]
    words_users={}
    count=0

    words_users_time=[]


    # process the data
    with open(meme_csv, 'rb') as csvfile:
        memecsv=csv.reader(csvfile)
        memecsv.next() # skip headers

        for row in memecsv:
            # extract text
            t=row[1]    
            count+=1

            timestamp=row[9]

            # regexp extract tweet entities
            mentions,urls,hashtags,clean=minetweet.extract_tweet_entities(t)
            
            # extract text 
            dico=nlp.extract_dictionary(clean)

            # remove stopwords and get clean dico
            clean_dico=nlp.remove_stopwords(dico)
            
            # remove more stopwords
            tmp_words=[w for w in clean_dico if w.encode('utf-8') not in stoplist and w[0] != "u" ]

            words_list+=tmp_words # global list for counter            

            # User diffusion graph
            user_diff=[]
            for mention in mentions:
                user_edges.append((row[0],mention))
                if mention not in user_diff : user_diff.append(mention)

                # retweeted_uid
            if row[7] != "" : 
                user_edges.append((row[7],row[0]))
                if row[7] not in user_diff : user_diff.append(row[7])


            words_series.append(tmp_words)

            for w in tmp_words :
                try :
                    words_users[w] += user_diff
                except KeyError:
                    words_users[w] = []
                    words_users[w] += user_diff

            words_users_time.append((tmp_words,user_edges,timestamp))



    '''
    # CSV processed
    edges_weighted=[str(p[0][0]+" "+p[0][1]+" "+str(p[1])) for p in Counter(user_edges).most_common()] # if p[1] > 1]

    print "Edges (raw files) : %d edges"%len(user_edges)
    print "Weighted edges %d"%len(edges_weighted)

    G = nx.read_weighted_edgelist(edges_weighted, nodetype=str, delimiter=" ",create_using=nx.DiGraph())

    N,K = G.order(), G.size()
    print "Nodes: ", N
    print "Edges: ", K

    jsondata["graph"]={}
    jsondata["graph"]["total_raw_edges"]=len(user_edges)
    jsondata["graph"]["total_nodes"]=N
    jsondata["graph"]["total_edges"]=K

    # init nodes
    d3nodes={}
    for n in G.nodes(data=True) : 
        d3nodes[ n[0] ]=n[1]
        d3nodes[ n[0]]["name"]=n[0]
        d3nodes[ n[0]]["province"]=get_province(n[0])


    # Clustering and degree coeficient
    #################################

    avg_deg = float(K)/N
    print "Average degree: ", avg_deg
    jsondata["graph"]["average_degree"]=avg_deg

    # Clustering coefficient of all nodes (in a dictionary)
    ccs = nx.clustering(G.to_undirected())

    # Average clustering coefficient
    avg_clust_coef = sum(ccs.values()) / len(ccs) # also : nx.algorithms.cluster.average_clustering(G.to_undirected())
    print "Average clustering coeficient: %f"%avg_clust_coef
    jsondata["graph"]["average_clustering_coeficient"]=avg_clust_coef

     # Communities
    # from http://perso.crans.org/aynaud/communities/ 
    ##################################################################

    jsondata["communities"]={}

    # Best partition
    best_partition = community.best_partition(G.to_undirected()) 
    modularity=community.modularity(best_partition,G.to_undirected())
    print "Modularity of the best partition: %f"%modularity
    print "Number of nodes in the best partition : ", len(set(best_partition.values())) 

    jsondata["communities"]={}
    jsondata["communities"]={}
    jsondata["communities"]["modularity"]=modularity
    jsondata["communities"]["number_of_communities"]=len(set(best_partition.values()))


    for node in best_partition:
        d3nodes[node]["community"]=best_partition[node]


    # CENTRALITIES 
    # http://toreopsahl.com/tnet/weighted-networks/node-centrality/
    #################################
    # Betweeness centrality
    # betweeness_centrality={}
    # Create ordered tuple of centrality data
    print "computing betweeness_centrality... (this may take some time)"

    if(N>10000) :cent_dict=nx.betweenness_centrality (G.to_undirected(),k=200)
    else : cent_dict=nx.betweenness_centrality (G.to_undirected())

    cent_items=[(b,a) for (a,b) in cent_dict.iteritems()]
    # add value to nodes
    for node in cent_dict: d3nodes[node]["btw_cent"]=cent_dict[node]
    '''
    '''
    # Sort in descending order 
    cent_items.sort() 
    cent_items.reverse() 

    # Highest centrality 
    jsondata["betweeness_centrality"]["top"]=[]
    for j,c in enumerate(cent_items[0:5]):
        print "Highest betweeness centrality :%.3f"%c[0]
        jsondata["betweeness_centrality"]["top"].append({"index": j, "value" :"%.3f"%c[0], "id" : c[1] })

    # Collect discretized distribution of centralities
    btw_cent_dist=[{"value":c[0],"count" :c[1] } for c in Counter(["%.3f"%c[0] for c in cent_items]).most_common()]

    jsondata["betweeness_centrality"]["distribution"]=btw_cent_dist
    jsondata["graph"]["average_betweeness_centrality"]=sum([c[0] for c in cent_items])/len(cent_items)
    '''
    '''
    # CREATE WORDS GRAPH
    ################################

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
    word_user_edges=[]
    for c in Counter(words_list).most_common(500):
        words_map[c[0]]=c[1]
        # create user > word graph
        for user in Counter(words_users[c[0]]).most_common():
            if user[1] > 2 : word_user_edges.append({"source": c[0], "target": user[0], "weight": user[1], "community" : best_partition[user[0]]})
    
    unique_nodes=[]
    for e in data_words["edges"]:
        if e["source"] not in unique_nodes : unique_nodes.append(e["source"]) 
        if e["target"] not in unique_nodes : unique_nodes.append(e["target"]) 

    data_words["nodes"]=[{"name" : node, "count": words_map[node]} for node in unique_nodes]

    
    # OUTPUT D3 GRAPH
    ################################

    # write d3js conversational graph
    # (only partial graph)
    min_weight=2
    d3_file=meme_path+"/"+meme_name+"_d3graph.json"

    d3data={}
    d3data["info"]=jsondata
    d3data["words"]=data_words
    d3data["words_user"]=word_user_edges
    
    d3data["nodes"]=[]
    d3data["edges"]=[ {"source":edge[0],"target":edge[1],"weight":edge[2]["weight"] } for edge in G.edges(data=True) if edge[2]["weight"] >= min_weight]
    
    d3_nodes_done=[]
    for edge in d3data["edges"]:
        if edge["source"] not in d3_nodes_done:
            d3_nodes_done.append(edge["source"])
            d3data["nodes"].append(d3nodes[edge["source"]])
        if edge["target"] not in d3_nodes_done:
            d3_nodes_done.append(edge["target"])
            d3data["nodes"].append(d3nodes[edge["target"]])

    d3data["users"]={}
    d3data["users"]["nodes"]=d3data["nodes"]
    del(d3data["nodes"])
    d3data["users"]["edges"]=d3data["edges"]
    del(d3data["edges"])

    # write d3js annotated graph
    with open(d3_file, 'w') as outfile:
        json.dump(d3data, outfile)
        print "json data have been saved to %s"%(d3_file)

    print "done in %.3fs"%(time()-tstart)

    # d3_file=meme_path+"/"+meme_name+"_d3graph.full.json"

    # d3fulldata={}
    # d3fulldata["info"]=jsondata
    # d3fulldata["nodes"]=[d3nodes[node] for node in d3nodes ]
    # d3fulldata["edges"]=[ {"source":edge[0],"target":edge[1],"weight":edge[2]["weight"] } for edge in G.edges(data=True)]

    # with open(d3_file, 'w') as outfile:
    #     json.dump(d3fulldata, outfile)
    #     print "full json data have been saved to %s"%(d3_file)

'''
for meme in meme_names:
    analyze_meme(meme)

print "Everything done in %.3fs"%(time()-t0)