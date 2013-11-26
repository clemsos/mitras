#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import time
from bson.code import Code
from lib.mongo import MongoDB
import numpy as np
import os.path

# Connect to Mongo
db=MongoDB("weibodata").db

# valid protomemes
valid_types =["hashtags","mentions","urls","phrase"]

def build_corpus(_type, _collection, _count, _destination):
    """
    Compute protomemes from tweets using MongoDB map reduce function
    see js files for details

    # Usage
    _type           String : should be a valid type of protomemes (see valid_types)
    _collection     String : is the mongo db source 
    _count          Int : number of tweets to process
    _destination    * String: name of the db to store results
                    * None  : return results as a dict

    """
    
    # check protomemes
    if _type not in valid_types:
        raise TypeError('Wrong type for protomemes. Valid types are :', valid_types)

    print "Processing %s"%_type
    print " starting map reduce on %d records" % _count
    t0 =time()

    # Load map and reduce function from js files
    mapjs=open("/home/clemsos/Dev/mitras/lib/mapreduce/map.js", "r").read()
    reducejs=open("/home/clemsos/Dev/mitras/lib/mapreduce/reduce.js", "r").read()

    
    # compile JS code
    mapper = Code(mapjs.replace("TO_BE_CHANGED", _type)) # apply type to js map file
    reducer = Code(reducejs)

    # print mapper

    t1=time()-t0

    if _destination == None :
        result = db[_collection].inline_map_reduce( mapper, reducer, limit=_count)
        print "haha"
        # print dict(result)
        return result
    else :
        result = db[_collection].map_reduce( mapper, reducer, _destination, limit=_count)

    print " %d new protomemes extracted" % result.count()
    print " stored in collection : %s " % db[_destination]
    print " done in %fs" % (time() - t0)
    print "-"*12
    print

def get_protomemes(_type, _count):
    """
    Return formatted protomemes from the db as a list
    _type   : None, get a mix of all types
            : String, should be a valid type (see valid_types)
    _count  : Int

    """

    pm_count=_count

    if _type != None:
        # check protomemes
        if _type not in valid_types:
            raise TypeError('Wrong type for protomemes. Valid types are :', valid_types)
        
        print _type

        my_db=db[_type]

        print "Total protomemes in the db :",
        print " %d"%my_db.count(),
        print "%s"%_type

        data=list(my_db.find().limit(_count))

        print "%d protomemes in this set"% (len(data))

        # try:
        #     print data[0]["value"]["type"]
        # except KeyError:
        #     print 'WARNING : --- type not defined'
        #     for value in data: 
        #         value["value"]["type"]=_type

    else :
        
        h_db=db["hashtags"]
        m_db=db["mentions"]
        u_db=db["urls"]

        print "Total protomemes in the db :"
        print " %d hashtags"%h_db.count()
        print " %d mentions"%m_db.count()
        print " %d urls"%u_db.count()
        print 10*"-"

        c=int(round(pm_count/3))
        h=list(h_db.find().limit(c))
        m=list(m_db.find().limit(c))
        u=list(u_db.find().limit(c))

        print "%d protomemes in this set"% (len(h)+len(m)+len(u)),
        print "(%d required) " % pm_count
        print " %d hashtags" % len(h)
        print " %d mentions" % len(m)
        print " %d urls" % len(u)
        print
        print 10*"-"

        
        # TODO : remove dirty hack (already added to map reduce)7
        # try:
        #     print m[0]["value"]["type"]
        # except KeyError:
        #     print 'WARNING : --- type not defined'
        #     for user in u: 
        #         user["value"]["type"]="user"
        #     for hashtag in h:
        #          hashtag["value"]["type"]="hashtag"
        #     for mention in u:
        #          mention["value"]["type"]="mention" 

        # concanate lists
        data=u+h+m

    # proto_count=h_db.count()
    # test acquisition
    # protomemes.get_protomemes("hashtags",100)

    # TODO : make list
    

    return data

def get_protomeme_by_id(_type, _id):
    # set the right db
    my_db=db[_type]

    query={ "_id": _id}
    data=list(my_db.find(query))

    return data

def get_protomemes_values_by_type(_collection,_type,_count):
    query = "value."+_type
    data=db[_collection].find( {},{ query: 1 } ).limit(_count)
    return list(data)

def create_txt_corpus_file(_count, _path):

    filename=_path+"/protomemes.txt"

    if not os.path.exists(filename):
        t0=time()
        
        # open file
        outfile = open(filename, "w")
        
        # get corpus from mongo
        # order = u+h+m
        collections =["urls","hashtags","mentions"]

        print " creating text corpus as file : %s"%filename
        for c in collections:
            print ' getting records from %s...'%c
            data=get_protomemes_values_by_type(c,"txt",_count)
            print ' got %d records'%len(data)
            for item in data:
                print>>outfile, item["value"]["txt"].encode('utf-8').split()
            print ' %s done '%c

        print " done in %.3fs"%(time()-t0)

    else:
        print " raw corpus already exists %s "%filename
        print 

def create_corpus_file(_type,_count,_path):

    # switch to a specific function for text
    if _type == "txt":
        create_txt_corpus_file(_count,_path)
        return

    filename=_path+"/protomemes."+_type
    
    if not os.path.exists(filename):
        t0=time()

        # open file
        outfile = open(filename, "w")
        
        # get corpus from mongo
        # order = u+h+m
        collections =["urls","hashtags","mentions"]

        print " creating %s corpus as file : %s"%(_type, filename)
        for c in collections:
            print ' getting records from %s...'%c
            data=get_protomemes_values_by_type(c,_type,_count)
            print ' got %d records'%len(data)
            for item in data:
                print>>outfile, item["value"][_type]
            print ' %s done '%c
        
        print " done in %.3fs"%(time()-t0)
        print
    else:
        print " raw corpus already exists %s "%filename
        print 
        
def create_labels_file(_path):
    if os.path.exists(_path+"/labels.txt"):
        print " labels already exist at %s/labels.txt"%_path
        pass
    else:
        # Store labels for future use
        print "Storing protomemes labels and ids for future reference"
        
        labels=[]
        print ' WARNING : protomeme type should be defined during map-reduce'
        for p in _protomemes:
            
            # TODO : add type to map/reduce _id  during protomemes creation
            # mytype= p["_id"]["type"] 
            # name=p["_id"]["name"]
            
            name=p["_id"]

            try:
                mytype= p["value"]["type"]
            except KeyError:
                # TODO : remove dirty hack (add to map reduce)
                # print 'WARNING : --- type not defined'
                if p["_id"][0] == "h":
                    mytype="urls"
                elif p["_id"][0] == "u":
                    mytype="mentions"
                else :
                    mytype="hashtags"

            labels.append((name, mytype))
        
        labels_path=_path+"/labels.txt"
        print " storing labels as file : %s"%labels_path
        outfile=open(labels_path,"wb")
        pickle.dump(labels, outfile)
        print
        
# DISCARDED : bcz mongo limit is 14MB per document...
def get_protomemes_values_by_type_as_array(_type,_count):
    # query = "value."+_type
    collections =["hashtags","mentions","urls"]

    t0=time()

    # TODO : change to map reduce to avoid max document size
    pipeline=[
        {"$group":{ "_id":"$value."+_type} }, 
        { "$limit":_count }]

    # print pipeline
    data=[]
    for c in collections:
        q = db.command('aggregate', c, pipeline=pipeline )
        data.append([ d["_id"] for d in q["result"] ])

    # print data
    final= data[0]+data[1]+data[2]

    print " Data was extracted succesfully in %fs" % (time() - t0)
    print " "+_type +" count :  %d results" % len(final)
    # data=db["hashtags"].find( {},{ query: 1 } ).limit(_count)
    return list(final)

