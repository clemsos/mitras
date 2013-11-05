#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from pymongo.errors import ConnectionFailure
from pymongo import Connection
# from ConfigParser import SafeConfigParser
#from pymongo.son_manipulator import AutoReference,NamespaceInjector
#from pymongo.code import Code

#config stuff
host= "localhost"
port = 27017

class mongoDB:

    def __init__(self, db):
        print """Connecting to MongoDB """

        try:
            # connect to mongo
            self.connection = Connection(host=host, port=port)

            # connect to db
            self.db = self.connection[db]
            print "Connected successfully MongoDB at %s:%s" %(host, str(port))

        except ConnectionFailure, e:
            sys.stderr.write("Could not connect to MongoDB: %s" % e)
            sys.exit(1)
    
    def save_data(self, data, collection):
        # create /select collection
        weiboData = self.db[collection]
        weiboData.insert(data, safe=True)
        print "stored in Mongo, collection: "+collection