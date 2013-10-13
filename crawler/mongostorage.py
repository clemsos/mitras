# -*- coding: utf-8 -*-
import sys
import os
from pymongo.errors import ConnectionFailure
from pymongo import Connection
from ConfigParser import SafeConfigParser
#from pymongo.son_manipulator import AutoReference,NamespaceInjector
#from pymongo.code import Code

class FileStorage():
    weiboDB = None

    def __init__(self,user):
        
        # config stuff
        # config = SafeConfigParser()
        # config.read( os.path.join(os.getcwd() + os.sep +  'settings.py') )
        # host = str(config.get('mongo', 'host'))
        # port = int(config.get('mongo', 'port'))

        host="localhost"
        port=27017
        self.db="weibo"
        # self.collection=user

        print """ Connecting to MongoDB """

        try:
            self.connection = Connection(host=host, port=port)
            print "Mongo connected successfully at %s:%s" % (host, port)
        except ConnectionFailure, e:
            sys.stderr.write("Could not connect to MongoDB: %s" % e)
            sys.exit(1)
        
    #follows or fans    
    def save_info(self, info):
        # data="uid\t昵称\t性别\t地区\t生日\t简介\t标签\n"
        # data="%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % tuple(info)
        #for k, v in info.iteritems():
            #self.info_f.write('%s：%s\n' % (k, v))

        print json.dumps(dict(info))

        #connect database
        weiboDB = self.connection[self.db]
        assert weiboDB.connection == self.connection
        print "Successfully set up a database handle"

        # create collection
        weiboData = weiboDB["info"]
        weiboData.insert(data, safe=True)
        print "stored in Mongo db : "+ self.db+", collection: "+"info"
        # return weiboDB

    def save_user(self, user_tuple):
        
        # data
        # data='%s：%s' % user_tuple + '\n'
        # print data
        print user_tuple
        print json.dumps(dict(user_tuple))

        #connect database
        weiboDB = self.connection[self.db]
        assert weiboDB.connection == self.connection

        # save
        weiboData = weiboDB["info"]
        weiboData.insert(data, safe=True)

    def save_weibo(self, weibo):
        
        print "saving weibo"
        # result = unicode(weibo['content'])
        # print weibo

        # if 'forward' in weibo:
        #     result += '// %s' % weibo['forward']
        # data=result + ' ' + str(weibo['ts']) + '\n'
        data=weibo
        print data

        #connect database
        weiboDB = self.connection[self.db]
        assert weiboDB.connection == self.connection

        # save
        weiboData = weiboDB["info"]
        weiboData.insert(data, safe=True)

    def save_users(self, user_tuples):
        for user_tuple in user_tuples:
            self.save_user(user_tuple)

    def error(self):
        f = open(os.path.join(self.path, "out",'errors.txt'), 'w+')
        try:
            f.write(str(self.uid) + '\n')
        finally:
            f.close()

    def complete(self):
        f = open(os.path.join(self.path, "out",'completes.txt'), 'w+')
        try:
            f.write(str(self.user) + '\n')
        finally:
            f.close()
