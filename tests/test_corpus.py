#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gensim import corpora
import codecs

path="/tmp/"
filename=path+"/blabla"
outfile = codecs.open(filename, "w", "utf-8")

def test_store_and_split_corpus():
    data=[["lala","lala","lala"],["lala","lala","lala"],["lala","lala","lala"]]
    for d in data:
        d1=str(d)[1:-1]
        # print d1
        print >> outfile, d1

    for t in open(filename, 'rb'):
        t1=t.split(", ")
        # print t1
        for m in t1:
            print m

def test_store_and_split_text_corpus():
    text=[ "hahah alsamù djskl dsds kljd", " dkqsl djqsk dqk dzae az", "opqs qù*ù&é" ]
    for d in text:
        d1=str(d.split())[1:-1]
        # print d1
        print >> outfile, d1

    for t in open(filename, 'rb'):
        t1=t.split(", ")
        # print t1
        for m in t1:
            print m

c="/tmp/pms/protomemes.txt"
def test_corpus():

    # f=open(c, "r")
    f=codecs.open(c, "r", "utf-8")

    for i,t in enumerate(f):
        if i == 3:
            break
        for x in t.split(", "):
            print type(x)

# compute path
def test_get_dic_length():
    dic_path='/tmp/pms/tweets.dict'
    # d=open(dic_path, "rb")
    print len(corpora.Dictionary.load(dic_path))

# test_corpus()
# corpus=corpora.MmCorpus("/tmp/pms/tweets.mm")
# print corpus


# fn="/tmp/blabla"
# f=open(fn, "r")
# print("hi there", file=outfile)

# s="u'\u6709\u9650\u516c\u53f8'"
# print type(s)
# u=unicode(s)
# print u
# print type( u ), len(u)
# # print repr(s)
# print type(u'\u6709\u9650\u516c\u53f8')
# .encode('utf-8').decode('utf-8')