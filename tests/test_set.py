#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, zipfile
import codecs
import pandas as pd
import lib.tweetminer as minetweet
from time import time

root_path="/home/clemsos/Dev/mitras/"
raw_data_path=root_path+"data/datazip/"
clean_data_path=root_path+"data/clean/"
training_set=root_path+"data/trainset.csv"

chunksize=1000

# init
needs_header=True
t0=time()

# clean training set
with open(training_set, 'w') as train:
    train.write("")

# loop through each csv
for path, subdirs, files in os.walk(raw_data_path):

     for filename in files:
        
        # open file store for training set
        with open(training_set, 'a') as train:
            
            if filename[-3:] == "zip" and filename[:4] == "week": # get only zip files 
                zip_path=path+filename
                raw_csvname=filename.split(".")[0]+".csv" 
                clean_csvname=clean_data_path+filename.split(".")[0]+".csv" 
                
                with zipfile.ZipFile(zip_path) as z: # open zip
                    f = z.open(raw_csvname) # read csv
                    csvfile=pd.read_csv(f, iterator=True, chunksize=chunksize) # parse csv with pandas
                    print "#"*20

                    # init training set
                    hashtrain = []
                
                    # reset clean data content
                    with open(clean_csvname, 'w') as toclean:
                        toclean.write("")

                    # create clean data
                    with open(clean_csvname, "a") as clean_csv:
                        
                        clean_needs_header=True
                        
                        # read csv chunk by chunk
                        for i,df in enumerate(csvfile): 

                            # print df.head()
                            if i==1 : break
                            print i

                            #save clean data
                            df.to_csv(clean_csv, mode='a', index=False, header=clean_needs_header)
                            clean_needs_header=False
                            
                            # save training file
                            # df_train.save(path+"tests/data/df_hashtags_week1.csv")
                    

print "done in %.3fs"%(time()-t0)

