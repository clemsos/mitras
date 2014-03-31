#!/usr/bin/env python
# -*- coding: utf-8 -*-
import elasticsearch
import unicodedata
import csv
import os

es = elasticsearch.Elasticsearch(["localhost:9200"])


results_path="/home/clemsos/Dev/mitras/results/"
meme_list_file=results_path+"2012_sina-weibo-memes_list.csv"


# parse data
with open(meme_list_file, 'rb') as csv_memelist:
    memelist=csv.reader(csv_memelist)
    keys,memes=[],[]
    for i,meme in enumerate(memelist):        
        if i==0: keys=meme
        temp_mm={}
        for j,col in enumerate(meme):
            temp_mm[keys[j]]=col
        memes.append(temp_mm)

# print memes

# Setup your variables
index_name="weiboscope_45_46"
meme_name=""
meme_keywords=["中国共产党第十八次全国代表大会","中共十八大","18大","十八大","代表大会"]

# meme_keywords=["表叔", "表哥","微笑局长", "杨达才"]
# meme_query="\"表叔\" OR \"表哥\" OR \"微笑局长\" OR \"杨达才\""
# results_path="/home/clemsos/Dev/mitras/results/"+meme_name

# build query
meme_query=""
for i,k in enumerate(meme_keywords):
    meme_query+='\"'+k+'\"'
    if i+1 < len(meme_keywords): meme_query+= " OR "

query={ "query": {
        "query_string": {
            "query": meme_query
         }
      }
    }

# Get the number of results
res = es.search(index=index_name, body=query)
data_size=res['hits']['total']
print("Total %d Hits" % data_size)
