#!/usr/bin/env python
# -*- coding: utf-8 -*-

from minimongo import Model, Index, configure
import json

# mongo db
configure(host="localhost", port=27017)
db_name="test"

class Tweet(Model):

    class Meta:
        # Here, we specify the database and collection names.
        # A connection to your DB is automatically created.
        database = db_name
        collection = "tweets"

        # Now, we programatically declare what indices we want.
        # The arguments to the Index constructor are identical to
        # the args to pymongo"s ensure_index function.
        # TODO : add indexes 
        indices = (
            # Index("mid"),
            Index("mid"),
            Index("hashtags"),
            Index("urls"),
            Index("mentions")
        )

    def __init__(self):
        
        self.mentions=[]
        self.urls=[]
        self.hashtags=[]
        self.entities=[] # NER entities

        # self.row=0 # store csv row

        # self.mid=rawTweet[0]
        # self.retweetFromPostId=rawTweet[1]
        # self.userId=rawTweet[2]
        # self.retweetFromUserId=rawTweet[3]
        # self.source=rawTweet[4]
        # self.hasImage=rawTweet[5]
        # self.txt=rawTweet[6]
        # self.geo=rawTweet[7]
        # self.created_at=rawTweet[8]
        # self.deleted_last_seen=rawTweet[9]
        # self.permission_denied=rawTweet[10]

        # self.clean=rawTweet[6] # txt without web entities for NLP
        
        # self.latitude=rawTweet[23]
        # self.longitude=rawTweet[24

    def get_tweet_entities(self):
        entities=[]
        for mention in self.mentions:
            entities.append(["mention", mention])
        for url in self.urls:
            entities.append(["url", url])
        for hashtag in self.hashtags:
            entities.append(["hashtag",hashtag])
        return entities

    def get_geo_entities(self):
        return self.tags.get("GPE")

    def get_loc_entities(self):
        return self.tags.get("LOC")

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

