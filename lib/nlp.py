#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ner
import jieba # import mmseg
import jieba.analyse


######################## 
# NLP + NER
# NER server should be up: ../see ner-server/
######################## 

# TODO : change to relative URL
stopwords_file="lib/stopwords/zh-stopwords"

class NLPMiner:
    def __init__(self): 

        print "init NLP toolkit"

        self.tagger = ner.SocketNER(host='localhost', port=1234)

        # parse list of stopwords
        self.stoplist=[i.strip() for i in open(stopwords_file)]

        # better support for traditional character
        # TODO : change to relative URL
        jieba.set_dictionary('lib/dict/dict.txt.big')


    def extract_keywords(self,txt):
        tags = jieba.analyse.extract_tags(txt, 20)
        # dico=extract_dictionary(txt)
        # tags=remove_stopwords(txt)
        return tags

    def extract_dictionary(self,txt):
        seg_list = jieba.cut(txt, cut_all=False)  # 搜索引擎模式
        # print ", ".join(seg_list)
        return list(seg_list)

    def remove_stopwords(self,txt):
        txt_wo_stopwords=[w for w in txt if w.encode('utf-8') not in self.stoplist and w.encode('utf-8') !=" "]
        return txt_wo_stopwords

    def extract_named_entities_from_dico(self,dico):
        # prepare Chinese seg for ENR
        # TODO : remove punctuation / stopwords ".","[","]",etc.
        seg_str=" ".join(dico)
        # get all entities 
        tags= self.tagger.get_entities(seg_str)
        return tags