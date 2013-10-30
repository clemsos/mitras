#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gkseg
import ner

text = '【哈尔滨雾霾舆论数据分析】哈尔滨PM2.5爆表，微博讨论声量在10月20日~21日持续上升。21日负面情绪指数大幅蔓延，微博成为当地人民表达负面情绪的一大渠道。疾病指数也在21日上午10:00~11:00达到第一个高峰，社交媒体数据与实际医疗数据的强相关性在此事件中得到体现。更多数据，请参见微博长图。'.decode('utf-8')
# http://weibo.com/2392261910/Afjg5e6bQ

# init
gkseg.init('gkseg/data/model.txt')
# for tagger to work, we need to launch Stanford NER Java socket server 
tagger = ner.SocketNER(host='localhost', port=1234)

#segment the sentence into a list of words
seg = gkseg.seg(text)
# for s in seg: 
#     print s.encode('utf-8')

#extract the important words from the sentence
# terms = gkseg.term(text)
# for t in terms: 
#     print t.encode('utf-8')

#label the sentence
# labels = gkseg.label(text)
# for l in labels: 
#     print l.encode('utf-8')

# prepare Chinese seg for ENR
seg_str =""
for s in seg: 
    seg_str += s.encode('utf-8')+" "
# print seg_str

# get all entities 
tags= tagger.get_entities(seg_str)
for t in tags: 
    print t.encode('utf-8')

# tags_json = tagger.json_entities(seg_text)
# print tags_json

gkseg.destroy()