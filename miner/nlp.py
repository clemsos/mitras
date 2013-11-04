#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ner
import jieba # import mmseg
import jieba.analyse


######################## 
# NLP + NER
# NER server should be up: ../see ner-server/
######################## 


def init_NLP(): 

    print "init NLP toolkit"
    tagger = ner.SocketNER(host='localhost', port=1234)

    # better support for traditional character
    jieba.set_dictionary('dict/dict.txt.big')


def extract_keywords(txt):
    tags = jieba.analyse.extract_tags(txt, 20)
    return tags

def extract_dictionary(txt):
    seg_list = jieba.cut(txt, cut_all=False)  # 搜索引擎模式
    # print ", ".join(seg_list)
    return list(seg_list)

def extract_named_entities(txt):

    #segment the sentence into a list of words
    seg=jieba.cut(txt)
    # print "Seg:", "/ ".join(seg)  # 全模式

    # prepare Chinese seg for ENR
    seg_str=" ".join(seg_txt)

    # get all entities 
    tags= tagger.get_entities(seg_str)

    return tags