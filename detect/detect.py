#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import re
# from scipy import spatial

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

# commit your changes
db.commit()

# get the number of rows in the resultset
numrows = int(cursor.rowcount)

######################## 
# Detect Entities 
######################## 

RTpattern =r"@([^:：,，\)\(（）|\\\s]+)"
URLPattern=r"\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^\p{P}\s]|/)))"
# hashtagPattern=r"[#]+([^|#]+)[#]"
# hashtagPattern=r"(^|\s)#([^\s]+)#"
hashtagPattern=r"#([^#\s]+)#"

regHash=re.compile(hashtagPattern)
# get and display one row at a time.
mentions=[]
urls=[]
hashtags=[]



for x in range(0,numrows):
    row = cursor.fetchone()
    # print row[0], "-->", row[2]
    tweet = row[2]
    for word in re.findall(RTpattern, tweet, re.UNICODE):
        mentions.append(word)
    for url in re.findall(URLPattern, tweet, re.UNICODE):
        urls.append(url[0])
    for hashtag in regHash.findall(tweet):
        print hashtag
        hashtags.append(hashtag)
        print tweet
        print '--' +hashtag


# for m in hashtags:
#     print m

print str(numrows)+" rows processed"
print str(len(mentions))+" mentions found"
print str(len(urls))+" urls found"
print str(len(hashtags))+" hashtags found"


######################## 
# Protomeme 
# a set of all tweets that contain the same entity
######################## 

class Protomeme():

    validEntities= ["hashtag","mention","url","phrase"];

    def __init__(self, entity):
        self.type=entity.type
        self.content=entity.content
        self.tweets=[]

    def addTweet(id):
        self.tweets.append(id);
        return

    def getType():
        return self.type

    def getContent():
        return self.content

    def save():
        # store to db
        return

def get_protomeme(entity):
    # request db
    return 
corpus =[]
for tweet in corpus:
    # entities
    for entity in tweets:
        # check if protomeme exists
        pm=get_protomeme(entity)
        if( pm == 0):
            pm=Protomeme(entity)
            pm.addTweet(tweet.id)
            pm.save()
        else:
            pm.addTweet(tweet.id)
            pm.save()

# extract terms

# Clustering : parse protomemes

    # Common user similarity
    def user_similarity(pI, pJ):
        pI # Protomeme
        pJ # Protomeme
        spatial.distance.cosine(pI, pJ)
        return

    # Common tweet similarity
    def tweet_similarity(pI, pJ):
        pass

    # Content similarity
    # Diffusion similarity
    # Geographic pattern similarity

# Combinations
