#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, zipfile
import pandas as pd
import lib.vectorizer as vectorizer

root_path="/home/clemsos/Dev/mitras/"
training_set=root_path+"data/train/trainset.csv"
train_path=root_path+"data/train/"

hashtags=pd.read_csv(training_set, sep=";", encoding="utf-8")
hashtags.rename({"mid":"diffusion"})

grouped=hashtags.groupby("hashtag", sort=True).agg(lambda x: x.tolist())

def flatten(arr):
    return [item for sublist in arr for item in sublist]

txt=flatten(grouped.phrase)
diffusion=flatten(grouped.diffusion)
tweets=grouped.mid
users=grouped.users

types=[(txt,"txt"),(diffusion,"diffusion"),(tweets,"tweets"),(users,"users")]

for mytype in types:

    filename=train_path+"train."+mytype[1]
    print filename

    if not os.path.exists(filename):
        # t0=time()        
        print " creating raw corpus : %s"%filename
        mytype[0].to_csv(filename)
        
    else:
        print " Raw corpus already exists %s "%filename
        print 
    