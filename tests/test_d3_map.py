#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
'''
import csv
import os 
import codecs
from time import time
from collections import Counter

from test_helpers import TestHelpers
helpers=TestHelpers()
helpers.add_relative_path()

from lib.users import UserAPI

import csv
from collections import Counter
from lib.users import UserAPI

# variables
map_title="Population of Sina Weibo users for a specific keyword"
map_desc="Based on Sina Weibo user profiles during a period of time. Data from weiboscope."
map_credits="by Clement Renaud - 2013"
tweets_file="/home/clemsos/Dev/mitras/data/sampleweibo.csv"
#tweets_file="/home/clemsos/Dev/mitras/lib/cities/usersample.csv"


# get user data
'''   
api=UserAPI()
user_provinces=[]
with open(tweets_file, 'rb') as csvfile:
    
    weibo_data=csv.reader(csvfile)
    csvfile.next() #skip csv header
    
    for tweet in weibo_data:
        # print tweet[2]
        province_code= api.get_province(tweet[2])
        user_provinces.append(api.provinces[province_code])


province_count=Counter(user_provinces).most_common()
# print province_count
for p in province_count:
    print p[0],p[1]
'''
province_count=[('Xianggang', 53), ('Guangdong', 24), ('Beijing', 10), ('Shanghai', 6), ('Taiwan', 6), ('Qita', 5), ('Hunan', 2), ('Yunnan', 2), ('Zhejiang', 2), ('Haiwai', 2), ('Shaanxi', 2), ('Jiangsu', 1), ('Anhui', 1), ('Guangxi', 1), ('Tianjin', 1), ('Henan', 1), ('Liaoning', 1), ('Fujian', 1)]

print province_count

# create HTML file with map
html_template="/home/clemsos/Dev/mitras/maps/map_template.html"

out_dir="/home/clemsos/Dev/mitras/maps"
out_filename=out_dir+"/meme_example.html"

# create html file

# parse var to js
jsvar="var data=["+','.join([ '["'+p[0]+'",'+str(p[1])+']' for p in province_count])+"];"
jsvar+="var title='"+map_title+"';"
jsvar+="var desc='"+map_desc+"';"
jsvar+="var credits='"+map_credits+"';"
print jsvar

# parse html
html=open(html_template, "r").read().replace("TO_BE_CHANGED", jsvar)
print html

# save htmlfile
with codecs.open(out_filename, "w", "utf-8") as outfile:
    outfile.write(html)