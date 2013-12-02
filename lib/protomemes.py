#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import time
from bson.code import Code
from lib.mongo import MongoDB
import numpy as np
import os.path
import codecs

# Connect to Mongo
db=MongoDB("weibodata").db

# valid protomemes
valid_types =["hashtags","mentions","urls","phrase"]

# Map-Reduce parser using MongoDB
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
    # TODO : change to relative path
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

#  Utils from creating rawcorpus
def get_protomemes_values_by_type(_collection,_type,_count):
    query = "value."+_type
    data=db[_collection].find( {},{ query: 1 } ).limit(_count)
    return list(data)

def create_txt_corpus_file(_count, _path):

    filename=_path+"/protomemes.txt"

    if not os.path.exists(filename):
        t0=time()
        
        # open file
        with codecs.open(filename, "w", "utf-8") as outfile:
        
            # get corpus from mongo
            # order = u+h+m
            collections =["urls","hashtags","mentions"]

            print " creating text corpus as file : %s"%filename
            for c in collections:
                print ' getting records from %s...'%c
                data=get_protomemes_values_by_type(c,"txt",_count)
                print ' got %d records'%len(data)
                for item in data:
                    outfile.write(str(item["value"]["txt"].split())[1:-1]+"\n")
                print ' %s done '%c

            outfile.close()
        print " done in %.3fs"%(time()-t0)
        print
    else:
        print " raw corpus already exists %s "%filename
        print 

# Main function to create raw corpus file
def create_corpus_file(_type,_count,_path):

    # switch to a specific function for text
    if _type == "txt":
        create_txt_corpus_file(_count,_path)
        return

    filename=_path+"/protomemes."+_type
    
    if not os.path.exists(filename):
        t0=time()

        # open file
        outfile = codecs.open(filename, "w", "utf-8")
        
        # get corpus from mongo
        # order = u+h+m
        collections =["urls","hashtags","mentions"]

        print " creating %s corpus as file : %s"%(_type, filename)
        for c in collections:
            print ' getting records from %s...'%c
            data=get_protomemes_values_by_type(c,_type,_count)
            print ' got %d records'%len(data)
            for item in data:
                outfile.write(str(item["value"][_type])[1:-1]+"\n")
            print ' %s done '%c
        
        outfile.close()
        print " done in %.3fs"%(time()-t0)
        print
    else:
        print " raw corpus already exists %s "%filename
        print 

# get all ids and type to create index
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

# create the actual index as a file
def create_protomemes_index_file(_path):
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

# API 
# using the protomemes index 
def get_protomemes_by_row(_path,x):
    labels=load_index_file(_path)
    row=labels[str(x)]
    # print len(labels)

    query= {"_id":row[0] }
    print query
    return list(db[row[1]].find(query))
    # record=db[row[1]].findById(row[0])
    # print record

def get_protomemes_ids_by_rows(_path,rows_id):
    # print type(rows_id)
    if type(rows_id) is not list:
        raise TypeError("x should be an array")

    labels=load_index_file(_path)
    
    # print type(labels)
    # rows=[]
    
    protomemes_ids={}
    for id in rows_id:
        row=labels[str(id)]
        # rows.append(row)
        try :
            protomemes_ids[row[1]].append(row[0])
        except KeyError:
            protomemes_ids[row[1]]=[]
            protomemes_ids[row[1]].append(row[0])

    return protomemes_ids


def get_row_by_protomemes(_path,_type,_id):
    labels=load_index_file(_path)
    return [int(l) for i,l in enumerate(labels) if labels[l]==(_id,_type)][0]

# data straight from db
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


# utils for API to parse index file
def load_index_file(_path):
    
    label_file=[i for i in open(_path+"/labels.txt").readlines()]
    labels={}

    for l in label_file:
        v=l.split()
        # print len(v)
        labels[v[0]]=(v[1],v[2])

    return labels