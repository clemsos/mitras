#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyelasticsearch import ElasticSearch
import pandas as pd
from time import time
import os, zipfile
import codecs

root_path="/home/clemsos/Dev/mitras/"
raw_data_path=root_path+"data/datazip/selected/"
pid_file=root_path+"data/tmp/csv_chunk"

t0=time()

# elastic search
chunksize=1000

# init ElasticSearch
es = ElasticSearch('http://localhost:9200/')

# try :
#     es.delete_index("weiboscope")
# except :
#     pass
# es.create_index("weiboscope")


# parse index name : 2 weeks per index to fasten search
weeks={}
for r in xrange(1,52,2):
    weeks[r]=weeks[r+1]="weiboscope_"+str(r)+"_"+str(r+1)

for w in  weeks: print w,weeks[w]

previous_chunk=0
for path, subdirs, files in os.walk(raw_data_path):
    
    # loop through each files
    i_file=0
    for filename in files: 
        # if i==1 : break

        file_is_ok=False

        # check if there is an ongoing task
        if filename[-10:] == "processing":
            
            file_is_ok=True

            # get previous
            with open(pid_file, "r") as pid:
                previous_chunk=int(pid.read())

            # get previous
            file_to_process_name=filename

        elif filename[-3:] == "zip" and filename[:4] == "week": # get only zip files

            file_is_ok=True
        
        if file_is_ok==True :
            t1=time()
            i_file+=1
        
            # flag the file
            zip_path=path+filename
            if filename[-10:] != "processing": 
                os.rename(zip_path, zip_path+".processing")
                zip_path=path+filename+".processing"

            raw_csvname=filename.split(".")[0]+".csv" 
            
            # read zipped csv files
            with zipfile.ZipFile(zip_path) as z: # open zip

                f = z.open(raw_csvname) # read csv
                csvfile=pd.read_csv(f, iterator=True, chunksize=chunksize) 
                
                week_number=filename.split(".")[0][4:]
                index_name=weeks[int(week_number)]
                # print index_name

                for i,df in enumerate(csvfile):

                    if i <= previous_chunk:
                        print i, "%d files, already indexed %s"%(i_file,raw_csvname)
                    else:
                        print i, "%d files, now indexing %s"%(i_file,raw_csvname)

                        # fix the date formatting
                        df["created_at"]=df["created_at"].str.replace(" ", "T")
                        
                        try :
                            
                            # fix encoding
                            df["text"]=df["text"].str.decode("utf-8")

                            # convert dataframe to json object
                            records=df.where(pd.notnull(df), None).T.to_dict()

                            # convert json object to a list of json objects
                            list_records=[records[it] for it in records]

                            # insert into elasticsearch
                            try :
                                es.bulk_index(index_name,"tweet",list_records)
                            except :
                                print "error with elasticsearch"
                                pass
                                
                        except :
                            print "encoding problem..."
                            pass

                        with open(pid_file, "w") as pid:
                            pid.write(str(i))

            print "%s processed in %.3fs"%(raw_csvname,time()-t1)

            # flag the file : done
            # os.rename(zip_path, zip_path+".done")
            os.remove(zip_path)
            
            # reset counters
            previous_chunk=0
            with open(pid_file, "w") as pid:
                pid.write(str(0))

print "Everything done in %.3fs"%(time()-t0)