#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
txt="文章在下面：http://t.cn/aE5XRc我倒不 http://t.cn/hlM77\xe9"
txt="http://t.cn/hlM77\xe9\x83\xa8\xe9\x83\xa8\xe9\x95\xb7\xe9\x83\x9d\xe9\x90\xb5\xe5\xb7\x9d\xe6\x89\xb9\xe8\xa9\x95".decode('utf-8')

URLPattern=r"\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^\p{6}\s]|/)))"
regURL=re.compile(URLPattern, re.UNICODE)

# for url in regURL.findall(txt):
#   print url[0][0:18]


urls= ['http://t.cn/haNbC\xe6', 'http://t.cn/SxdqHu']

def sanitize_url(txt):
    valid_utf8 = True
    try:
        txt.decode('utf-8')
    except UnicodeDecodeError:
        valid_utf8 = False
        return txt[:-1]
    return txt
    # print valid_utf8

for u in urls:
    print sanitize_url(u).encode('utf-8')