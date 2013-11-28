#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main file showing the whole clustering process in a single file.

"""
import os
import lib.tweetminer as minetweet
from lib.nlp import NLPMiner


# Download and store all files from HKU server
os.system('wget -r "http://147.8.142.179/datazip/"')

# 
# init libraries
# PROCESS all tweets in csv file
nlp=NLPMiner()
# extract_and_store_tweets(csv_file,nlp, minetweet)
path=

    