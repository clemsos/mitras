#!/usr/bin/env python
# -*- coding: utf-8 -*-

import miner.tweetminer as minetweet
import re
txt="文章在下面：http://t.cn/aE5XRc我倒不"

URLPattern=r"\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^\p{6}\s]|/)))"
regURL=re.compile(URLPattern, re.UNICODE)

for url in regURL.findall(txt):
	print url[0][0:18]


