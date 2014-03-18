#!/usr/bin/env python
# -*- coding: utf-8 -*-
import elasticsearch
import unicodedata
import csv

es = elasticsearch.Elasticsearch(["localhost:9200"])

# Setup your variables
index_name="weiboscope"
meme_keywords="杜甫很忙"
csv_file="杜甫很忙.csv"
chunksize=1000

# Get the number of results
res = es.search(index=index_name, body={"query": {"match": { "text" : "'杜甫很忙'" }}})
data_size=res['hits']['total']
print("Total %d Hits" % data_size)

# get headers
headers=[value for value in res['hits']['hits'][0]["_source"]]

# Open a csv file and write the stuff inside
with open(csv_file, 'wb') as csvfile: 

    filewriter = csv.writer(csvfile)

    # create column header row
    filewriter.writerow(headers)

    # Get numbers of results 
    for chunk in xrange(0,data_size,chunksize):

        
        # display progress as percent
        per=round(float(chunk)/data_size*100, 1)

        # request data
        res=es.search(index=index_name, body={"query": {"match": { "text" : "'杜甫很忙'" }}}, size=chunksize, from_=chunk)

        print"%.01f %% %d Hits Retreived" % (per,chunk)

        if res['hits']['hits'][0]["_score"] < 1 : break

        for sample in res['hits']['hits']: 
            row=[]
            for id in sample["_source"]:
                if type(sample["_source"][id]) == unicode : data = sample["_source"][id].encode("utf-8") 
                else : data = sample["_source"][id] 
                row.append(data)

            filewriter.writerow(row)

print "Done. Data saved in %s"%csv_file