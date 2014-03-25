#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
This is a test for user db interactions
'''
import csv
from collections import Counter

from test_helpers import TestHelpers
helpers=TestHelpers()
helpers.add_relative_path()

from lib.users import UserAPI

api=UserAPI()
result = api.get_province("uHRWEYSX0")
print result


userdata_file="/home/clemsos/Dev/mitras/lib/cities/usersample.csv"
def test_write_users(userdata_file): 

    with open(userdata_file, 'rb') as csvfile:
        i=0

        user_data=csv.reader(csvfile)
        csvfile.next() #skip csv header
        
        for row in user_data:
            api.create_user(row)
            i+=1

    print "%d users saved"%i



api=UserAPI()

tweets_file="/home/clemsos/Dev/mitras/data/sampleweibo.csv"
#tweets_file="/home/clemsos/Dev/mitras/lib/cities/usersample.csv"

user_provinces=[]
with open(tweets_file, 'rb') as csvfile:
    
    weibo_data=csv.reader(csvfile)
    csvfile.next() #skip csv header
    
    for tweet in weibo_data:
        province_code= api.get_province(tweet[2])
        
        if province_code !=None : user_provinces.append(api.provinces[province_code])
        

print user_provinces
province_count=Counter(user_provinces)
print province_count