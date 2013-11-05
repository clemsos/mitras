#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid

class Protomeme:
    def __init__(self):

        valid_types=['mention','hashtag','url','phrase','geo']

        self.quoted_users=[]
        self.type=""
        self.entity=""
        self.tweets=[]

        print "protomeme created"
    
    # def create_uid(self):
        # uuid.uuid3(uuid.NAMESPACE_DNS, self)

    def set_type(self,_type):
		if _type not in self.valid_types:
			raise Error('protomeme has invalid type', _type)
		self.type=_type

    def set_entity(self,_entity):
    	self.entity=_entity
    	return _entity

    def add_tweet(self,_tweet):
    	self.tweets.append(_tweet)

    def add_user(self,_user):
    	self.quoted_users.append(_user)

    def to_JSON(self):
    	return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def to_user_vector(self):
        pass

    def to_text_vector(self):
        pass

    def to_diffusion_vector(self):
        pass