#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Testing meme creation
'''

import csv

from time import time
from test_helpers import TestHelpers

helpers=TestHelpers()
helpers.add_relative_path()
from lib.mongo import MongoDB
from lib.memes import *

# from lib.memes import *

# vars
path="/home/clemsos/Dev/mitras/data/out"
# db=MongoDB("weibodata").db # Connect to Mongo

def test_list_of_dict_to_csv(_rows,_csv_filepath):
    
    # get keys for csv value
    keys=_rows[0].keys()
    print " extracting %s from tweets"%(keys)

    # write to csv
    with open(csv_file,'w') as f: # writes the final output to CSV
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writer.writerow(keys)
        dict_writer.writerows(_rows)

    print " csv has been stored as %s"%_csv_filepath

def test_list_to_csv(_keys,_rows,_csv_filepath):
    
    # get keys for csv value
    # keys=_rows[0].keys()

    print " extracting %s from tweets"%(_keys)
    # write to csv
    with open(_csv_filepath,'w') as f: # writes the final output to CSV
        csv_out=csv.writer(f)
        csv_out.writerow(_keys) # add header
        for row in _rows:
            csv_out.writerow(row)

    print " csv has been stored as %s"%_csv_filepath

def test_meme_to_gephi_csv(_name,_dir_path):
    t0=time()

    # get meme data
    query={ "name" : _name}
    meme=list(db["memes"].find(query))[0]
    print " tweets in meme :  %d" % len(meme["tweets"])

    # 
    nodes=[]
    edges=[]

    for i,t in enumerate(meme["tweets"]):
        nodes.append( (t["userId"],"user"+str(i)) )

        # add mentions
        for m in t["mentions"]:
            edges.append((t["userId"],t["userId"]))
        
        # add RTs
        if t["retweetFromUserId"] != "": 
            edges.append((t["retweetFromUserId"],t["userId"]))

    list_to_csv(["Id", "Label"],nodes,_dir_path + '/'+_name+'_nodes.csv')
    list_to_csv(["Source","Target"],edges,_dir_path +'/'+_name+'_edges.csv')

    print " done in %fs" % (time() - t0)

meme_to_gephi_csv("吴奇隆",path)