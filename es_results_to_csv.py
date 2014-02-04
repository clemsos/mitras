#!/usr/bin/env python
# -*- coding: utf-8 -*-
import elasticsearch
import unicodedata
import csv

es = elasticsearch.Elasticsearch(["10.1.1.1:9200"])
# this returns up to 500 rows, adjust to your needs
res = es.search(index="YourIndexName", body={"query": {"match": {"title": "elasticsearch"}}},500)
sample = res['hits']['hits']

# then open a csv file, and loop through the results, writing to the csv
with open('outputfile.tsv', 'wb') as csvfile:   
    filewriter = csv.writer(csvfile, delimiter='\t',  # we use TAB delimited, to handle cases where freeform text may have a comma
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
    # create column header row
    filewriter.writerow(["column1", "column2", "column3"])    #change the column labels here
    # fill columns 1, 2, 3 with your data 
    col1 = hit["some"]["deeply"]["nested"]["field"].decode('utf-8')  #replace these nested key names with your own
    col1 = col1.replace('\n', ' ')
    # col2 = , col3 = , etc...
    for hit in sample: 
        filewriter.writerow([col1,col2,col3])