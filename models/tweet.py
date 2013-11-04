#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

class Tweet:
    def __init__(self, rawTweet):
        
        self.mentions=[]
        self.urls=[]
        self.hashtags=[]

        self.keywords=[]  # keywords
        self.tags=[] # NER entities

        self.clean=rawTweet[7] # txt without web entities for NLP

        self.mid=rawTweet[1]
        self.retweetFromPostId=rawTweet[2]
        self.userId=rawTweet[3]
        self.retweetFromUserId=rawTweet[4]
        self.source=rawTweet[5]
        self.hasImage=rawTweet[6]
        self.txt=rawTweet[7]
        self.geo=rawTweet[8]
        self.created_at=rawTweet[9]
        self.deleted_last_seen=rawTweet[10]
        self.permission_denied=rawTweet[11]
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

