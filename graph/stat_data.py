#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from csv import reader
from multiprocessing import Process

# head -n5000 /media/Data/Taf/phD/Data/weibo/HKU/weiboscope/week1.csv > sampleweibo.csv
f='sampleweibo.csv'

# read as dataframe
data=pd.read_csv(f)
print data.columns

print "--------------------------"
# read as csv
csv_in = open(f,  'rU')
myreader = reader(csv_in)


# Loop over the reader object to process one row at a time:
items_list = []
for row in myreader:
    items=[]
    for item in row:
        items.append(item)
    items_list.append(item)

print str(len(items_list)) + " items processed"

# If the csv file size is  greater than RAM, use multiprocess
# from  http://articlesdictionary.wordpress.com/2013/09/29/read-csv-file-in-python/

# See interesting topic : http://stackoverflow.com/questions/2359253/solving-embarassingly-parallel-problems-using-python-multiprocessing/2364667#2364667
