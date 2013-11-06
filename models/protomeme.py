#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import uuid
import json
from minimongo import Model, Index, configure

# mongo config
configure(host="localhost", port=27017)
db_name="protomemes"

class Protomeme(Model):

    class Meta:
        # Here, we specify the database and collection names.
        # A connection to your DB is automatically created.
        database = db_name
        collection = "week1"

        # Now, we programatically declare what indices we want.
        # The arguments to the Index constructor are identical to
        # the args to pymongo"s ensure_index function.
        # indices = (
        #     Index("a"),
        # )

    def __init__(self):

        self.valid_types=['hashtags','mentions','urls','txt','entities']

        # description
        self.desc={}
        self.desc.type=""
        self.desc.content=""
        
        # content
        self.tweets=[]
        self.users=[]
        self.txt=[]
        self.entities=[]

        # print "protomeme created"
    
    # def create_uid(self):
        # uuid.uuid3(uuid.NAMESPACE_DNS, self)

    def set_description(self,_type,_txt):
        if _type not in self.valid_types:
			raise ValueError('protomeme has invalid type', _type)
        self.desc.type=_type
        self.desc.content=_txt

    def get_description(self):
        stats={}
        stats['type']=self.desc.type
        stats['content']=self.desc.content
        stats['tweets']=str(len(self.tweets))
        stats['users']=str(len(self.users))
        stats['txt']=str(len(self.txt))
        stats['entities']=str(len(self.entities))

        return stats
        # return desc

    def print_description(self):
        
        stats=self.get_description()
        
        print " "
        print 10*"#"
        print "type     :"+stats["type"]
        print "content  :"+stats["content"]
        print "tweets   :"+stats["tweets"]
        print "users    :"+stats["users"]
        print "txt      :"+stats["txt"]
        print "entities :"+stats["entities"]

    def get_query(self):

        # check if type has been setup
        if self.desc.type == "" :
            raise ValueError('Protomeme type should be setup first')

        if self.desc.type=="geo" or self.desc.type=="txt":
            raise Exception('Not implemented yet...')
        else:
            return { self.desc.type:  self.desc.content }

        # process queries by case
        # if self.desc.type == 'hashtags':
        # elif self.desc.type == "mentions":
        #     return { "mentions":  self.desc.content }
        # elif self.desc.type == "urls":
        #     return { "urls":  self.desc.content }

        # else :


    def add_tweet(self,_tweet):
    	self.tweets.append(_tweet)

    def add_user(self,_user):
    	self.users.append(_user)

    def to_JSON(self):
    	return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def to_user_vector(self):
        pass

    def to_text_vector(self):
        pass

    def to_diffusion_vector(self):
        pass