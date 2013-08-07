##Weibo Crawler

this is a weibo crawler to crawl weibo user's info and relationship,
I only need these information for my project. 
This repository is inspired by [chineking](https://bitbucket.org/chineking/weibocrawler/wiki/Home).

###To use this repository

1. new a file settings.py similar to settings.py.sample, use a valid weibo account and password.
2. use ``python main.py [uids]`` to crawler user's information with a list of uids.


##  Feed keywords from Google Spreadsheets 

### Spreadsheets

Keywords

* https://docs.google.com/spreadsheet/ccc?key=0ArNEXxu0b66PdHpNS3o1bnVDOVNPRHFKcnoxNEd5cXc#gid=0

* CSV : https://docs.google.com/spreadsheet/pub?key=0ArNEXxu0b66PdHpNS3o1bnVDOVNPRHFKcnoxNEd5cXc&output=csv

* JSON : https://spreadsheets.google.com/feeds/list/0ArNEXxu0b66PdHpNS3o1bnVDOVNPRHFKcnoxNEd5cXc/od6/public/values?alt=JSON

* XML : https://spreadsheets.google.com/feeds/list/0ArNEXxu0b66PdHpNS3o1bnVDOVNPRHFKcnoxNEd5cXc/od6/public/basic?alt=rss

China Digital Times :

* https://docs.google.com/spreadsheet/pub?key=0Aqe87wrWj9w_dFpJWjZoM19BNkFfV2JrWS1pMEtYcEE&output=csv
* Editable : https://docs.google.com/spreadsheet/ccc?key=0Aqe87wrWj9w_dFpJWjZoM19BNkFfV2JrWS1pMEtYcEE#gid=0


### Convert spreadsheets to json using Google Apps

Method from [HOWTO](http://blog.pamelafox.org/2013/06/exporting-google-spreadsheet-as-json.html) by P.Fox using [this gist](https://gist.github.com/pamelafox/1878143)


TCP-DUMP

tcpdump -i wlan0 src net 192 | grep IP | awk -F " " '{print $3}' 
>> file.txt

# FreeWeibo.com
* https://twitter.com/CensoredWeibo
* https://freeweibo.com/en/weibo/%E5%A4%A7%E9%BB%84%E9%B8%AD?censored
* https://github.com/percyalpha/News/wiki/%E8%87%AA%E7%94%B1%E5%BE%AE%E5%8D%9A%E5%A2%99%E5%86%85%E9%95%9C%E5%83%8F%E8%BF%9E%E6%8E%A5

http://research.jmsc.hku.hk/social/search.py/sinaweibo/#lastdeleted