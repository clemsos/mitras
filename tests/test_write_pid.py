#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import csv
# from pyelasticsearch import ElasticSearch
import pandas as pd
import os 

root_path="/home/clemsos/Dev/mitras/data/"
raw_csvname=root_path+"sampleweibo.csv"
pid_file=root_path+"csv_chunk"
raw_data_path=root_path+"datazip/"

chunksize=1000
previous_chunk=0
file_to_process_name=""

# previous_chunk=4
# print previous_chunk

# read zipped csv files
for path, subdirs, files in os.walk(raw_data_path):
    
    # loop through each files
    for i_file, filename in enumerate(files): 
        # if i==1 : break

        # check if there is an ongoing task
        if filename[-10:] == "processing":
            
            # get previous
            with open(pid_file, "r") as pid:
                previous_chunk=int(pid.read())

            # get previous
            file_to_process_name=filename

        elif filename[-3:] == "zip" and filename[:4] == "week": # get only zip files
            file_to_process_name=filename

        print file_to_process_name, previous_chunk
        
        zip_path=path+filename
        raw_csvname=filename.split(".")[0]+".csv" 
        
        # flag the file "processing"
        # os.rename(zip_path+".processing", zip_path+".processing.done")



        # reset
        previous_chunk=0