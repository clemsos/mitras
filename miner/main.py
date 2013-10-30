#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import re
from scipy import spatial
import pandas.io.sql as psql
import json
import pandas as pd
import numpy as np
import gkseg
import ner

######################## 
# IMPORT DATA
######################## 

nbRecords=str(300)

# connect to Mysql
db = MySQLdb.connect(host="localhost", user="root", passwd="password",
db="weibodata")
db.set_character_set('utf8')

cursor = db.cursor()
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')

# execute SQL select statement
statement="SELECT * FROM  `tweets_umap2012_complete` LIMIT 0 ," +nbRecords
cursor.execute(statement)

# print some stats through pandas query
# df = psql.frame_query(statement, con=db)
# print df.describe
# print "matrix :"+ str(df.shape)

# commit your changes
db.commit()

# get the number of rows in the resultset
numrows = int(cursor.rowcount)

# array to store all our tweets
tweets=[]

class Tweet:
    def __init__(self, rawTweet):
        self.mentions=[]
        self.urls=[]
        self.hashtags=[]

        self.keywords=[]  # keywords
        self.tags=[] # NER entities

        # self.creationTime=rawTweet[0]
        self.id=rawTweet[1]
        self.created_at=str(rawTweet[0])
        self.txt=rawTweet[2]
        self.source=rawTweet[3]
        self.favorite=rawTweet[4]
        # self.truncated=rawTweet[5]
        self.replyToPostId=rawTweet[6]
        self.replyToUserId=rawTweet[7]
        # self.replyToUsername=rawTweet[8]
        self.retweetFromPostId=rawTweet[9]
        self.retweetFromUserId=rawTweet[10]
        # self.retweetFromUsername=rawTweet[11]
        # self.thumbnailPic=rawTweet[12]
        # self.bmiddlePic=rawTweet[13]
        # self.originalPic=rawTweet[14]
        self.geo=rawTweet[15]
        self.userId=rawTweet[16]
        self.mid=rawTweet[17]
        self.reposts_count=rawTweet[18]
        self.comments_count=rawTweet[19]
        # self.annotation=rawTweet[20]
        # self.json=rawTweet[21]
        # self.crawledFromSampleUsers=rawTweet[22]
        self.latitude=rawTweet[23]
        self.longitude=rawTweet[24]

        # print self.creationTime
        # print "tweet created"

    def get_entities(self):
        entities=[]
        for mention in self.mentions:
            entities.append(["mention", mention])
        for url in self.urls:
            entities.append(["url", url])
        for hashtag in self.hashtags:
            entities.append(["hashtag",hashtag])
        return entities

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

######################## 
# Detect Tweet Entities 
######################## 

RTpattern =r"@([^:：,，\)\(（）|\\\s]+)"
URLPattern=r"\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^\p{P}\s]|/)))"
# hashtagPattern=r"[#]+([^|#]+)[#]"
# hashtagPattern=r"(^|\s)#([^\s]+)#"
hashtagPattern=r"#([^#\s]+)#"
regHash=re.compile(hashtagPattern)

mentions=[]
urls=[]
hashtags=[]

# get and process  one row at a time.
for x in range(0,numrows):
    row = cursor.fetchone()
    tweet= Tweet(row)

    for mention in re.findall(RTpattern, tweet.txt, re.UNICODE):
        tweet.mentions.append(mention)
        mentions.append(mention)

    for url in re.findall(URLPattern, tweet.txt, re.UNICODE):
        tweet.urls.append(url[0])
        urls.append(url[0])

    for hashtag in regHash.findall(tweet.txt):
        tweet.hashtags.append(hashtag)
        hashtags.append(hashtag)
        
    # print tweet
    tweets.append(tweet) 

# showTweets()
print str(len(tweets))+" tweets processed"
print "mentions:"+str(len(mentions))+ " urls:"+str(len(urls)) + " hashtags:"+str(len(hashtags))
print "total entities found: " +str(len(mentions)+ len(urls) + len(hashtags))
print tweets[1].to_JSON()


######################## 
# NLP
######################## 
print 'start NLP'

gkseg.init('gkseg/data/model.txt')
tagger = ner.SocketNER(host='localhost', port=1234)

for t in tweets:

    txt=t.txt.decode('utf-8')

    #segment the sentence into a list of words
    seg = gkseg.seg(txt)

    #extract the important words from the sentence
    terms = gkseg.term(txt)
    t.keywords=terms

    # for term in terms: 
    #     print term.encode('utf-8')

    # prepare Chinese seg for ENR
    seg_str =""
    for s in seg: 
        seg_str += s.encode('utf-8')+" "

    # get all entities 
    tags= tagger.get_entities(seg_str)
    t.tags=tags
    # for t in tags: 
    #     print t.encode('utf-8')

#label the sentence
# labels = gkseg.label(text)
# for l in labels: 
#     print l.encode('utf-8')

for t in tweets:
    geo=t.tags.get("LOC")
    if geo is not None:
        for g in geo:
            print g.encode('utf-8')

######################## 
# Protomemes
# extract memes primary entities from tweets 
######################## 

# general array to store 
# TODO convert this to a DB
proto={}

# Protomeme db
# ex protomemes {id:134543134, name:"hoho", type:"url", tweets:[mid1, mid2 ..., midx]}
proto["memes"]=[]

# Protomeme keystore
# TODO : convert this to a REDIS key value store
# ex  protomemes:type:url {name:"hoho", id:134543134}
proto["hashtag"]=[]
proto["mention"]=[]
proto["url"]=[]

class Protomeme:

    validEntities= ["hashtag","mention","url","phrase"];

    def __init__(self, entity):
        # print entity
        self.type=entity[0]
        self.content=entity[1]
        self.tweets=[]

        self.addToKeystore()
        self.saveToDB()
        
    def addTweet(self,id):
        self.tweets.append(id);
        return

    def getType(self):
        return self.type

    def getContent(self):
        return self.content

    def getUsers(self):
        users=[]
        for t in self.tweets:
            users.append(t.userId)
        return users

    def getCoords(self):
        coords=[]
        for t in self.tweets:
            coord=(t.latitude,t.longitude)
            coords.append(coord)
        return coords
    
    def getTexts(self):
        texts=[]
        for t in self.tweets:
            texts.append(t.txt)
        return texts

    def addToKeystore(self):
        proto[entity[0]].append(self)

    def saveToDB(self):
        proto["memes"].append(self)

    def save(self):
        # TODO : store to db
        # print 'protomeme created'
        pass

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


    # Turn Protomemes into vector
        
def get_protomeme(entity):
    # TODO : request keystore to find this
    for i,p in enumerate(proto["memes"]):
        if p.type == entity[0] and p.content==entity[1]:
            return proto["memes"][i]
    return 0 

# create protomemes
def create_protomemes(tweets):
    for t in tweets:
        # print t.get_entities()
        for entity in t.get_entities():
            # check if protomeme exists
            pm=get_protomeme(entity)
            if(pm==0):
                pm=Protomeme(entity)
                pm.addTweet(t)
                pm.save()
            else:
                pm.addTweet(t)
                pm.save()

    print "total protomemes: " +str(len(proto["memes"]))

# for p in proto["memes"]:
#     if len(p.tweets) > 3:
#         print p.to_JSON()

######################## 
# Compute Protomemes
# memes as sum of vectors
######################## 


for p1 in proto["memes"]:
    for p2 in proto["memes"]:
        if p1 is not p2:
            u1=np.array(p1.getUsers())
            u2=np.array(p2.getUsers())
            # print spatial.distance.cosine(u1,u2)
#     # print p.getUsers()
#     # print p.getCoords()
#     # print p.getTexts()

#     pass


# Common tweet similarity
def tweet_similarity(tweets_1, tweets_2):
    for p1 in proto["memes"]:
        for p2 in proto["memes"]:
            if(p1 is not p2):
                print spatial.distance.cosine(p1.tweets, p2.tweets)
    pass

# Common user similarity
def user_similarity(pI, pJ):
    pI # Protomeme
    pJ # Protomeme
    spatial.distance.cosine(pI, pJ)
    return

# Content similarity

# cosine similarity between 2 tweets TF-IDF vectors

# Diffusion similarity
# Geographic pattern similarity

# Combinations
