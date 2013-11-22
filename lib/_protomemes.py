#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.mongo import MongoDB
from time import time
import io, json

# Variables
collection="week1"  
proto_count=10000 # number of tweets to process. Use zero to process all

# Connect to Mongo
db=MongoDB("weibodata").db
data=db[collection]
tweets_count=data.count()
print
print str(tweets_count)+" tweets in the db"
print 10*"-"

# Compute protomemes for each type
# Protomeme.valid_types=['hashtags','mentions','urls','phrases','entities']

# Mongo
def get_protomemes(_type, _count, _collection):
    print 'Getting ' + _type + ' protomemes...'

    t0=time()

    pipeline = [
        { "$project" : { 
            _type : 1,
            "mid" : 1,
            "userId" : 1,
            "mentions" : 1,
            "retweetFromUserId" : 1,
            "dico" :1
            }
        },
        { "$limit" : _count },
        { "$unwind" : "$"+_type } ,
        { "$unwind" : "$mentions"}, 
        { "$unwind" : "$dico"}, 
        { "$group" : {
            "_id"       : "$"+_type, 
            "count"     : { "$sum" : 1 } ,         # tweets count
            "tweets"    : { "$addToSet" : "$mid"}, # tweet Ids
            "txt"       : { "$push" : "$dico"},
            "users"     : { "$addToSet" : "$userId"}, # unique Ids    
            "poster"    : { "$push" : "$userId"},
            "mentions"  : { "$push" : "$mentions"},
            "rts"       : { "$push" : "$retweetFromUserId"}
            } 
        }
    ]

    q = db.command('aggregate', _collection, pipeline=pipeline )


    t1=time()-t0
    
    print " Data was extracted succesfully in %fs" % (time() - t0)
    print " "+_type +" count :  %d results" % len(q["result"])
    # print " Matrix : n_samples: %d, n_features: %d" % tfidf_matrix.shape
    print

    # get protomemes data
    protomemes = q["result"]
    print 'Computing diffusion graph vector'
    t1=time()-t0
    for p in protomemes:
        count=len(p["poster"])
        p["diffusion"]=[]

        for i in range(count):
            if p["poster"][i] != '':
                p["diffusion"].append(p["poster"][i]) 
            if p["mentions"][i] != '':
                p["diffusion"].append(p["mentions"][i]) 
            if p["rts"][i] != "":
                p["diffusion"].append(p["rts"][i]) 

    print " done in %fs" % (time() - t0)
    print
    # print protomemes[0]["diffusion"]
    # print protomemes
    return protomemes

# hashtags_proto= get_protomemes("hashtags",collection)

# compute graph



# get_protomemes("urls",collection)

# get_protomemes("hashtags")
# get_protomemes("mentions")

# TODO
# create_protomemes("txt",proto_count)
# create_protomemes("entities",proto_count)



###############################################################
#USELESS
'''
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
    proto_list=create_protomemes_list(_type,_count)

    # Create Protomemes
    print 10*"-"
    print "creating protomemes..."

    start_proto = timeit.default_timer() # measure time
    results=[] # store logs

    t0 = time() # measure time
    
    elapsed_proto=time()-t0
    for h in proto_list:
        proto_stats=create_protomeme(_type,h)
        results.append(proto_stats)

    # some console log 
    print str(len(results))+" protomemes created in "+ str(elapsed_proto)+" s"

    # write log to JSON for later analysis
    write_to_JSON_file(results,log_file)
    print "results stored in file : "+log_file

# Create a list of all unique protomemes in corpus (hashtags, mentions, etc.)
def create_protomemes_list(_type,_nb_items):
    
    print 'Creating a list of all '+_type+' in the collection :'+collection

    # measure time
    start = time()

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
    
    elapsed = time()- start

    # log
    print
    print "nb of "+_type+" processed : "+str(_nb_items)
    print "unique  "+_type+"         : "+str(len(unique_results))
    print "processed in "+str(elapsed)+"s"
    print 10*"-"

    # print hashtags
    return unique_results
'''