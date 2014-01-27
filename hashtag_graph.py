#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, zipfile
import codecs
import pandas as pd
import lib.tweetminer as minetweet
from lib.nlp import NLPMiner
from lib.mongo import MongoDB

import lib.visualizer as viz
import csv
import json,bson
from time import time
import numpy as np
from bson.code import Code
from bson.objectid import ObjectId
from lib.memes import list_to_csv
from collections import Counter
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from mpl_toolkits.basemap import Basemap
from matplotlib import cm

root_path="/home/clemsos/Dev/mitras/"
raw_data_path=root_path+"data/datazip/"
clean_data_path=root_path+"data/clean/"
train_path=root_path+"data/train/"
gv_path=root_path+"out/gv/"
viz_path=root_path+"out/viz/"
gephi_path=root_path+"out/gephi/"
map_path=root_path+"out/maps/"
# training_set=root_path+"data/train/trainset.csv"

# sample_scale=4 #number of iterations
chunksize=5000

# init
t0=time()
nlp=NLPMiner()
# needs_header=True
# init_files=[True,True,True,True,True]

# Connect to Mongo
db=MongoDB("weiboclean").db
# db=MongoDB("test").db
# where the raw data is
collection=db["tweets"]

# get corpus length
tweets_count=collection.count()
print str(tweets_count)+" tweets in the db"
print 10*"-"

# add of stop-hahstags t remove most common occurence
stop_hashtags_file=root_path+"/lib/stopwords/stop_hashtags"
stop_hashtags=[i.strip() for i in open(stop_hashtags_file)]



###
# CREATE HASHTAGS LIST 
###

t1=time()
print "Extracting top hashtags from the dataset..."
count=0
# save_hashtag=None
save_hashtag="go"

destination= "hashtags"
hashtag_collection=db[destination]
hashtag_collection.ensure_index("value.count")


h=hashtag_collection.find().sort("value.count",-1).limit(1000)
top_hashtags=list(h)

with open("hashtags","w") as out_file:
    for r in top_hashtags: 
        if r["_id"].encode("utf-8") not in stop_hashtags : out_file.write(r["_id"].encode('utf-8')+"\n")

top_hashtags_ok=[ ( h["_id"].encode('utf-8'),h["value"]["count"]) for h in top_hashtags if h["_id"].encode('utf-8') not in stop_hashtags ]

# print top_hashtags_ok
list_to_csv(["Id","Count"],top_hashtags_ok,"top_hashtags.csv")


print "%d/%d hahstags are ok "%(len(top_hashtags_ok), len(list(top_hashtags)))

print "list of main hashtags saved "
print "done in %.3fs"%(time()-t1)


def flatten(arr):
    return [item for sublist in arr for item in sublist]


top_hashtags=[]
with open("top_hashtags.csv","rb") as top_hashtags_file:
    for i,line in enumerate(csv.reader(top_hashtags_file, delimiter=",",skipinitialspace=True)):
        if (i != 0) : top_hashtags.append(line)
        

###
# PARSE DATA AND VISUALIZE GRAPH
###

t2=time()
print "Generating data sets"
print "%d hashtags data set in the db"%(len(top_hashtags))

# prepare data for visualization
for i,h in enumerate(top_hashtags):
    # if i == 1 : break
    meme_name=h[0]
    meme_count=int(float(h[1])) 
    meme_tweets=collection.find({"hashtags":meme_name})
    print i, "/", len(top_hashtags), meme_name,meme_count

    # compute data from raw
    geo={}
    geo["lats"], geo["longs"]=[],[]
    diff=[]

    for tweet in meme_tweets:

        # DIFFUSION
        # mentions
        for mention in tweet["mentions"]:
            try :
                mention.decode("utf-8")
                if tweet["uid"] != mention :
                    diff.append({"from":tweet["uid"],"to":mention})
            except UnicodeEncodeError:
                pass
        
        # rt
        if type(tweet["retweeted_uid"]) is not float :
            # if math.isnan(tweet["retweeted_uid"]) is False :
                diff.append({"from":tweet["retweeted_uid"],"to":tweet["uid"]})

        # GEO DATA
        if type(tweet["geo"]) is not float : 
            geo["lats"].append(tweet["geo"][0])
            geo["longs"].append(tweet["geo"][1])
    
    # print geo

    # create graphviz file
    gv_filepath=gv_path+meme_name+".gv"
    viz_filepath=viz_path+meme_name+".png"

    with open(gv_filepath,'w') as f:

        line = "digraph mentions {\n" # open .gv file
        f.write(line)

        for i,action in enumerate(diff):
            if action["from"] != action["to"]:
                line = '"'+action["from"]+'"'+"->"+'"'+action["to"]+'"'+"\n"
                
                f.write(line)

        line = "}"+"\n" # close .gv file
        f.write(line)  
    print "graph file saved at : %s "%gv_filepath

    # draw with graphviz
    command = "sfdp -Gbgcolor=black -Ncolor=white -Ecolor=white -Nwidth=0.05  -Nheight=0.05 -Nfixedsize=true -Nlabel='' -Earrowsize=0.4 -Gsize=75 -Gratio=fill -Tpng " + gv_filepath + " > " + viz_filepath
    
    os.system(command)
    print "viz graph saved as %s"%viz_filepath

    # create gephi files
    edges=[]
    tmp_nodes={}
    
    for action in diff:
        edges.append( (action["from"],action["to"]) )

        tmp_nodes[ action["to"] ]= "user_"+action["to"] 
        tmp_nodes[ action["from"] ]= "user_"+action["from"] 
    
    nodes=[(tmp_nodes.keys()[i],tmp_nodes.values()[i]) for i in range(0, len(tmp_nodes))]

    gephi_nodes_path=gephi_path+meme_name+"_nodes.csv"
    gephi_edges_path=gephi_path+meme_name+"_edges.csv"

    list_to_csv(["Id", "Label"],nodes,gephi_nodes_path)
    list_to_csv(["Source","Target"],edges,gephi_edges_path)

    '''
    # DRAW MAP
    # dimensions
    w,h=20,12
    m_path=map_path+meme_name

    # Create a figure with size
    fig = plt.figure(figsize=(w,h))

    # Create a canvas and add the figure to it.
    canvas = FigureCanvas(fig)
    mapfig = fig.add_subplot(111)

    # miller projection
    m= Basemap(projection='mill',lon_0=-50,lat_0=60,resolution='l')

    # plot coastlines, draw label meridians and parallels.
    m.drawmapboundary(fill_color='black') # fill to edge
    m.drawcountries()
    m.fillcontinents(color='white',lake_color='black',zorder=0)

    # Scatter plot posts
    x, y = m(geo["longs"],geo["lats"])
    m.scatter(x,y,10,marker="o",cmap=cm.cool,alpha=0.7,color='red')

    # add legend
    plt.title(meme_name+" : Geotagged posts")

    # canvas.print_figure(m_path,dpi=200)
    # fig.savefig(m_path+".pdf")

    print "Map file has been save as PNG & PDF : %s "%m_path
    plt.show()
    '''
        
print "Data files created."    
print "done in %.3fs"%(time()-t2)
print 


