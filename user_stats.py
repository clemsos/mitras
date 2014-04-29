#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from lib.users import UserAPI

api=UserAPI()

results_path="/home/clemsos/Dev/mitras/results/"
nb_of_users_by_provinces_file=results_path+"nb_of_users_by_provinces.json"

nb_of_users_by_provinces={}
total=0

# count
for i,province in enumerate(api.provinces):
    # if i==1: break
    c=api.db.find({"province": province}).count()
    nb_of_users_by_provinces[province]=c
    print "%d users in %s"%(c,api.provinces[province])
    total+=c

print "%d users in %d provinces"%(total,i+1)

# percent
percent_of_users_by_provinces={}
total_percent=0
for province in api.provinces:
    p=(float(nb_of_users_by_provinces[province])/total)*100
    percent_of_users_by_provinces[province]=p
    total_percent+=p
print "%d total percent"%total_percent

data=[]
for province in api.provinces:
    data.append({
            "name":api.provinces[province],
            "percent":percent_of_users_by_provinces[province],
            "count":nb_of_users_by_provinces[province]
            })

# write json data
with open(nb_of_users_by_provinces_file, 'w') as outfile:
    json.dump({"nb_of_users_by_provinces":data}, outfile)
    print "json data have been saved to %s"%(nb_of_users_by_provinces_file)