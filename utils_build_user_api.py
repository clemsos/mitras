#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
from lib.users import UserAPI

api=UserAPI()

userdata_file="/home/clemsos/Dev/mitras/data/datazip/others/userdata.csv"
# userdata_file="/home/clemsos/Dev/mitras/lib/cities/usersample.csv"
# number of lines : 14,388,386 users

with open(userdata_file, 'rb') as csvfile:
    i=0

    user_data=csv.reader(csvfile)
    csvfile.next() #skip csv header
    print "Storing users... Please Wait."

    for row in user_data:
        api.create_user(row)
        i+=1
        
print "%d users saved"%i