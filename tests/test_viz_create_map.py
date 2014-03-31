#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import os 
import codecs
from time import time
from collections import Counter
from lib.users import UserAPI

# variables
meme_name="thevoice"
map_title="Population of Sina Weibo users for The Voice"
map_desc="Based on Sina Weibo user profiles info. Data from HKU Weiboscope."
map_credits="by Clement Renaud - 2013"
map_units="Volume of tweets (per 100)"

tweets_file="/home/clemsos/Dev/mitras/results/"+meme_name+"/"+meme_name+".csv"

#tweets_file="/home/clemsos/Dev/mitras/lib/cities/usersample.csv"


# get user data   
api=UserAPI()
user_provinces=[]
with open(tweets_file, 'rb') as csvfile:
    
    weibo_data=csv.reader(csvfile)
    csvfile.next() #skip csv header
    print "processing tweets..."
    for tweet in weibo_data:
        # print tweet[0]
        province_code= api.get_province(tweet[0])
        # print province_code
        try :
            user_provinces.append(api.provinces[province_code])
        except KeyError :
            print "error"



# print province_count
province_count=[(p[0],p[1]/100) for p in Counter(user_provinces).most_common()]


# create HTML file with map
html_template="/home/clemsos/Dev/mitras/d3-china-map/map_template.html"

out_dir="/home/clemsos/Dev/mitras/results"
out_filename=out_dir+"/map_user"+meme_name+".html"

# create html file

# parse var to js
jsvar="var data=["+','.join([ '["'+p[0]+'",'+str(p[1])+']' for p in province_count])+"];"
jsvar+="var title='"+map_title+"';"
jsvar+="var desc='"+map_desc+"';"
jsvar+="var credits='"+map_credits+"';"
jsvar+="var units='"+map_units+"';"
print jsvar

# parse html
html=open(html_template, "r").read().replace("TO_BE_CHANGED", jsvar)
# print html

# save htmlfile
with codecs.open(out_filename, "w", "utf-8") as outfile:
    outfile.write(html)

print "HTML map created at "+out_filename