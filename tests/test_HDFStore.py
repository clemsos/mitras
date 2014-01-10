#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from time import time 
path="/home/clemsos/Dev/mitras/"
file_path=path+"data/datazip/week10.csv"
store_path=path+"tests/data/tweets.h5"


dtypes={
    "mid"                   :   object,
    "retweeted_status_mid"  :   object,
    "uid"                   :   object,
    "retweeted_uid"         :   object,
    "source"                :   object,
    "image"                 :   object,
    "text"                  :   object,
    "geo"                   :   object,
    "created_at"            :   object,
    "deleted_last_seen"     :   object,
    "permission_denied"     :   object
    }


chunksize=2000

t0=time()

csvfile=pd.read_csv(file_path, iterator=True, chunksize=chunksize, dtype=dtypes)
store = pd.HDFStore(store_path,mode='w')

print "data stored in %s"%store

for i,df in enumerate(csvfile):
    if i==1000 : break
    print i, df
    store.append('df',df,min_itemsize = 600)

store.close()

print
print "done in %.3fs"%(time()-t0) 