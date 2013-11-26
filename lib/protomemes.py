#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import time
from bson.code import Code
from lib.mongo import MongoDB

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


class ProtomemeCorpus(object):
    def __iter__(self):
        for line in open(corpus_path):
            # assume there's one document per line, tokens separated by whitespace
            yield dictionary.doc2bow(line.lower().split())
    

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
