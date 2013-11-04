#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

######################## 
# Detect Tweet Entities 
######################## 


def init_tweet_regex():
    
    # patterns 
    RTpattern =r"@([^:：,，\)\(（）|\\\s]+)"
    URLPattern=r"\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^\p{P}\s]|/)))"
    # hashtagPattern=r"[#]+([^|#]+)[#]"
    # hashtagPattern=r"(^|\s)#([^\s]+)#"
    hashtagPattern=r"#([^#\s]+)#"

    # compile reg
    regHash=re.compile(hashtagPattern, re.UNICODE)
    regRT=re.compile(RTpattern, re.UNICODE)
    regURL=re.compile(URLPattern, re.UNICODE)

    print 'init tweet entities regex'

    return regHash, regRT, regURL

# init 
regHash, regRT, regURL = init_tweet_regex()

def extract_tweet_entities(txt):
    
    mentions=[]
    urls=[]
    hashtags=[]
    clean=txt

    for mention in regRT.findall(txt):
        # t.mentions.append(mention)
        m="@"+mention
        clean=txt.replace(m,"")
        mentions.append(mention)

    for url in regURL.findall(txt):
        # t.urls.append(url[0])
        clean=clean.replace(url[0],"")
        urls.append(url[0])

    for hashtag in regHash.findall(txt):
        # t.hashtags.append(hashtag)
        h='#'+hashtag+'#'
        clean=clean.replace(h,"")
        hashtags.append(hashtag)

    return mentions,urls,hashtags,clean



