#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lib.mongo import MongoDB
from models.user import User
import csv

class UserAPI:

    def __init__(self): 
        print "User API instance"
        # Connect to Mongo
        self.db=MongoDB("tweets").db["weibousers"]
        print "Total users in the db : %d"%self.db.count()
        print '-'*12

        # fetch cities
        provinces_file="/home/clemsos/Dev/mitras/lib/cities/provinces.csv"
        self.provinces={}

        with open(provinces_file, 'rb') as csvfile:
            
            provinces_data=csv.reader(csvfile)
            
            for row in provinces_data:
                self.provinces[row[0]]=row[1]


    def create_user(self, data):
        try: 
            province =self.provinces[data[1]]
        except: 
            province=0

        u=User()
        u.uid=data[0]
        u.province=data[1]
        u.gender=data[2]
        u.verified=data[3]
        u.save() # store to mongo
        # print "user %s saved"%data[0]

    def get_user(self,_uid):
        user=self.db.find_one({"uid":_uid}) #.limit(c)
        return user

    def get_province(self,_uid):
        user=self.db.find_one({"uid":_uid}) #.limit(c)
        if user != None:
            return user["province"]
        else : 
            return None