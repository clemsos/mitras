#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from test_helpers import TestHelpers
helpers=TestHelpers()
helpers.add_relative_path()

from lib.protomemes import get_protomemes, build_corpus, get_protomemes_values_by_type, get_protomemes_values_by_type_as_array

coll="week1"

class TestProtomemes(unittest.TestCase):

    def setUp(self):
        print "Testing protomemes"
        self.count = 1

    def test_get_protomemes(self):
        proto=get_protomemes("hashtags",self.count)
        self.assertEqual(len(proto),self.count)

    def test_build_corpus_and_store_to_db(self):
        proto=build_corpus("urls", "week1", 1 ,"test_urls")
        self.assertTrue(proto == None)

    def test_build_corpus_inline(self):
        proto=build_corpus("urls", "week1", 1 , None)
        self.assertTrue(proto != None)

    def test_corpus_should_have_tweets(self):
        proto=build_corpus("urls", "week1", 100, None)
        self.assertTrue(proto[0]["value"]["tweets"])
        print proto

    def test_get_protomemes_values_by_type(self):
        data=get_protomemes_values_by_type("users",1)    
        self.assertTrue(data[0]["value"]["users"])
        # there should be no text, just users
        with self.assertRaises(KeyError):
            data[0]["value"]["txt"]

    def test_get_protomemes_values_by_type_as_array(self):
        data=get_protomemes_values_by_type_as_array("txt",1)
        self.assertTrue(len(data) == 1)


    def protomemes_should_have_type(self):
        proto=get_protomemes("hashtags",1)
        self.assertTrue(proto[0]["value"]["type"] == "hashtag")


if __name__ == '__main__':
    unittest.main()

# print "%d protomemes obtained." % len(protomemes)
# print 

# db=MongoDB('weibodata').db
# from lib.mongo import MongoDB
# proto = build_corpus("hashtags",coll,2000, None)

# print len(proto)
# for p in proto:
#     print "*"*12
#     try :
#         print p["_id"]
#         print p["value"]["type"]
#     except KeyError:
#         print "                  error"
#         # print p["_id"]


# # test creation
# protomemes.build_corpus("hashtags", week1, 1000 ,"test_hashtags")
# protomemes.build_corpus("mentions", week1, 1000 ,"test_mentions")
# protomemes.build_corpus("urls", week1, 1000 ,"test_urls")

# # test acquisition
# pms=protomemes.get_protomemes(100)
# print len(pms)
# for p in pms:
#     print p


# h_db=db["test_hashtags"]
# m_db=db["test_mentions"]
# u_db=db["test_urls"]
# # proto_count=h_db.count()

# print "Total in the db :"
# print " %d hashtags"%h_db.count()
# print " %d mentions"%m_db.count()
# print " %d urls"%u_db.count()
# print 10*"-"
# pm_count=1000

# c=int(round(pm_count/3))
# h=list(h_db.find().limit(c))
# m=list(m_db.find().limit(c))
# u=list(u_db.find().limit(c))

# print "%d protomemes in this set"% (len(h)+len(m)+len(u)),
# print "(%d required) " % pm_count
# print " %d hashtags" % len(h)
# print " %d mentions" % len(m)
# print " %d urls" % len(u)
# print
# print 10*"-"

