#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import os

root_path="/home/clemsos/Dev/mitras/out/hashtags/"
data_path=root_path+"data/"

def list_to_csv(_keys,_rows,_csv_filepath):
    
    with open(_csv_filepath,'w') as f: # writes the final output to CSV
        csv_out=csv.writer(f)
        csv_out.writerow(_keys) # add header
        for row in _rows:
            csv_out.writerow(row)

    print " csv has been stored as %s"%_csv_filepath

# get hashtags list
hashtags_path=data_path+"top_hashtags.csv"
with open(hashtags_path, 'rb') as cs_file:
    cs_file.next() # skip header
    csv_hash=csv.reader(cs_file)
    hashtags=[word for word in csv_hash]

hashtags_path_2=data_path+"top_hashtags_2.csv"
with open(hashtags_path_2, 'rb') as cs_file:
    cs_file.next() # skip header
    csv_hash=csv.reader(cs_file)
    hashtags+=[word for word in csv_hash]

print "%d hashtags in files"%len(hashtags)

# get censored
censored_list_path=os.path.dirname(os.path.dirname(root_path))+"/SensitiveSinaWeiboSearchTerms.csv"

censored_words=[]
with open(censored_list_path, 'rb') as cs_file:
    csv_censor=csv.reader(cs_file)
    censored_words=[word[0] for word in csv_censor]

# image size 
total=0
hashtags_stats=[]
for i,h in enumerate(hashtags):
    censored=0
    if h in censored_words: censored=1
    hashtag=h[0]
    count=int(float(h[1]))
    try :
        # TODO : improve granularity by scanning csv rows count, not size
        size=os.path.getsize(root_path+"/0-1000/gv/"+hashtag+".gv")
        hashtags_stats.append((hashtag, count, size, censored))
        total+=1
    except :
        try :
            # TODO : idem
            size=os.path.getsize(root_path+"/1000-2000/gv/"+hashtag+".gv")
            hashtags_stats.append((hashtag, count, size, censored))
            total+=1
        except :
            pass

print 
print "TOTAL :%d results"%len(hashtags_stats)

list_to_csv(["label","tweets","conversation","censored"],hashtags_stats,root_path+"hashtags_stats.csv")
