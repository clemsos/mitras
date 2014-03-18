#!/usr/bin/env python
# -*- coding: utf-8 -*-
import elasticsearch
import csv
import unicodedata

# init es client
es = elasticsearch.Elasticsearch(['http://localhost:9200/'])

# get column names
indices=es.indices.get_mapping(index="weiboscope",doc_type="tweet")
colnames=indices["tweet"]["properties"]

# Replace the following Query with your own Elastic Search Query
res = es.search(index="weiboscope", body=
{
  "query": {
    "filtered": {
      "query": {
        "query_string": {
            "query": "permission_denied:exists"
         }
      },
      "filter": {
        "numeric_range": {
          "created_at": {
            "gte": "2012-02-05",
            "lte": "2012-04-20"
          }
        }
      }
    }
  }
}, size=3669)  #this is the number of rows to return from the query... to get all queries, run script, see total number of hits, then set euqual to number >= total hits

print("Got %d tweets" % res['hits']['total'])

sample = res['hits']['hits']
with open(outfile, 'wb') as csvfile: 

    filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    
    # create header row
    filewriter.writerow([c for c in colnames])    

    for hit in sample:   #switch sample to randomsample if you want a random subset, instead of all rows
        # print hit["_source"]
        # print
        col=[]
        for colname in colnames:
            # print colname, hit["_source"][colname]

            if colnames[colname]["type"] == 'string' and hit["_source"][colname] is not None:
                    try:
                        col.append(hit["_source"][colname].encode('utf-8'))
                    except UnicodeDecodeError:
                        pass
            else:
                try:
                   col.append(hit["_source"][colname])
                except:
                    col.append("")

        filewriter.writerow(col)

print "Tweet data saved as : %s"%outfile
