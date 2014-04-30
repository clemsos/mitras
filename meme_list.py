#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv,os,json


results_path="/home/clemsos/Dev/mitras/results/"
meme_file=results_path+"2012_sina-weibo-memes_list.csv"
meme_list_file=results_path+"2012_sina-weibo-memes_list.json"

# parse data
meme_list=[]
with open(meme_file, 'rb') as memecsv:

    memelist=csv.reader(memecsv, delimiter=",")
    print memelist
    # poplist.next() # skip headers
    keys=[]
    for i,row in enumerate(memelist) : 
        if(i==0): keys=row
        else: 
            meme={}
            for j,key in enumerate(keys): 
                meme[key]=row[j]
            meme_list.append(meme)

print meme_list

with open(meme_list_file, 'w') as outfile:
        json.dump({"memes":meme_list}, outfile)
        print "json data have been saved to %s"%(meme_list_file)

            