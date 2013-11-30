#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import time
from test_helpers import TestHelpers
import codecs

helpers=TestHelpers()
helpers.add_relative_path()

from lib.mongo import MongoDB

# Connect to Mongo
db=MongoDB("weibodata").db

stats=[
    (44382,"hashtags"),
    (398392,"mentions"),
    (264651,"urls")
]

# x is a row number
def get_label(x):

    r1=stats[0][0]
    r2=r1+stats[1][0]
    r3=r2+stats[2][0]
    
    # print r1,r2,r3
    print x
    if x in range(0,r1):
        print stats[0][1]

    elif x in range(r1,r2):
        print stats[1][1]

    elif x in range(r2,r3):
        print stats[2][1]

    else:
        raise ValueError(" x=%d out of index range , max : %d"%(x,stats[2][0])) 

def test_get_label():
    get_label(200) # 1
    get_label(100000) # 2
    get_label(600000) # 3 
    get_label(1000000)# ValueError

def get_protomemes_ids(_collection,_count):

    pm_count=_count
 
    coll=db[_collection]

    print "Total %s in the db : %d"%(_collection,coll.count())
    print 10*"-"

    h=coll.find({},{"__id":1, "value.type":1}).limit(_count)

    # print "%d protomemes in this set"% (len(h)+len(m)+len(u)),
    print "(%d required) " % pm_count

    print
    print 10*"-"

    return list(h)

def create_labels_file(_path):
    t0=time()
    # request protomemes, only object id
    count=44382+398392+264651

    # get corpus from mongo
    # order = u+h+m
    collections =["urls","hashtags","mentions"]

    # protomemes=get_protomemes_ids(None,count)

    filename=_path+"/labels.txt"

    # open file
    with codecs.open(filename, "w", "utf-8") as outfile:

        # write labels as follow : (row_id, id, type)
        print " creating corpus as file : %s"%(filename)
        outfile.write("[")

        # loop through each collection to create db
        c=0
        for coll in collections:
            print ' getting records from %s...'%c
            protomemes=get_protomemes_ids(coll,count)
            print ' got %d records'%len(protomemes)

            for i,p in enumerate(protomemes):
                try :
                    mytype= p["value"]["type"]
                except KeyError:
                    mytype
                    # TODO : remove dirty hack (add to map reduce)
                    # print 'WARNING : --- type not defined'
                    if p["_id"][0] == "h":
                        mytype="urls"
                    elif p["_id"][0] == "u":
                        mytype="mentions"
                    else :
                        mytype="hashtags"
                c+=1
                outfile.write(str(c)+" "+p["_id"]+" "+str( mytype)+"\n")
                # outfile.write()
        
        outfile.write("")

    print " done in %.3fs"%(time()-t0)
    print

def load_labels_file(_path):
    
    label_file=[i for i in open(_path+"/labels.txt").readlines()]
    labels={}

    for l in label_file:
        v=l.split()
        # print len(v)
        labels[v[0]]=(v[1],v[2])

    return labels

def get_protomemes_by_row(_path,x):
    labels=load_labels_file(_path)
    row=labels[str(x)]
    # print len(labels)

    query= {"_id":row[0] }
    print query
    return list(db[row[1]].find(query))
    # record=db[row[1]].findById(row[0])
    # print record

def get_row_by_protomemes(_path,_type,_id):
    labels=load_labels_file(_path)
    # print labels
    r= [l for i,l in enumerate(labels) if labels[l]==(_id,_type)][0]
    return r  # print labels[x]

# create_labels_file("/tmp")
# load_labels_file("/tmp")

# row=get_row_by_protomemes("/tmp","urls", 'http://t.cn/GVuKh')
# print row

row=get_row_by_protomemes("/tmp","hashtags", '吴奇隆')
print row # 278393
protomemes=get_protomemes_by_row("/tmp",row)