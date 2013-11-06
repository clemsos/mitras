#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint
from models.protomeme import Protomeme
from lib.mongo import MongoDB
import timeit
import io, json

# Variables
collection="week1"  
proto_count=0 # number of protomemes to extract. Use zero to process all

# Connect to Mongo
db=MongoDB("weibodata").db
data=db[collection]
tweets_count=data.count()
print 10*"-"
print str(tweets_count)+" tweets in the db"

Protomeme
def create_protomemes_list(_type,_nb_items):
    
    # measure time
    start = timeit.default_timer()

    # get all tweets with at least 1 hashtag
    # query = {'$where' : "this.hashtags.length > 0"}
    query = {_type: {"$not": {"$size": 0} } }
    tweets=data.find(query).limit(_nb_items)

    # TODO : use redis queue?
    unique_results=[]

    # create list of unique hashtags
    for t in list(tweets):  
        for h in t[_type]:
            if h not in unique_results: 
                unique_results.append(h)
    
    stop = timeit.default_timer()
    elapsed=stop-start

    # log
    print 10*"-"
    print "nb of "+_type+" processed : "+str(_nb_items)
    print "unique  "+_type+"         : "+str(len(unique_results))
    print "processed in "+str(elapsed)+"s"

    # print hashtags
    return unique_results

def create_protomeme(_type, _content):
    
    # create protomeme
    proto= Protomeme()

    # validate type
    if _type not in proto.valid_types:
        raise ValueError('protomeme has invalid type', _type)

    # set desc
    proto.set_description(_type,_content)
    
    # Find all elements in db
    query= proto.get_query() # get query based on protomeme type
    print query 
    tweets= list(data.find(query).limit(tweets_count)) 

    # add each tweet info to protomeme
    for tweet in tweets:
        proto.tweets.append(tweet['mid'])   # messages
        proto.txt.append(tweet['dico'])  # text
        
        proto.users.append(tweet['userId']) # users
        
        # add mentions
        for m in tweet['mentions']:
            proto.users.append(m) # users

        # TODO : add RT/mentions graph
        # proto.tweets.append(tweet['graph'])  # graph

    # save to protomemes db
    proto.save()

    # return basic info about the protomemes
    proto.print_description()
    return proto.get_description()

def write_to_JSON_file(_data,_file):
    json_results=json.dumps(_data,ensure_ascii=False)
    with io.open(_file, 'w', encoding='utf-8') as f:
      f.write(json_results)

def create_protomemes(_type,_count):
    
    log_file='log/'+_type+'.json'

    # Create a list of all unique protomemes in corpus (hashtags, mentions, etc.)
    print 'Creating a list of all '+_type+' in the collection :'+collection
    proto_list=create_protomemes_list(_type,_count)

    print 10*"-"

    # Create Protomemes
    print "creating protomemes..."

    start_proto = timeit.default_timer() # measure time
    results=[] # store logs

    for h in proto_list:
        proto_stats=create_protomeme(_type,h)
        results.append(proto_stats)

    # measure time
    stop_proto = timeit.default_timer()
    elapsed_proto=stop_proto-start_proto

    # some console log 
    print str(len(results))+" protomemes created in "+ str(elapsed_proto)+" s"

    # write log to JSON for later analysis
    write_to_JSON_file(results,log_file)
    print "results stored in file : "+log_file

# Compute protomemes for each type
# Protomeme.valid_types=['hashtags','mentions','urls','phrases','entities']

create_protomemes("hashtags",proto_count)
# create_protomemes("mentions",proto_count)
# create_protomemes("urls",proto_count)

# TODO
# create_protomemes("txt",proto_count)
# create_protomemes("entities",proto_count)