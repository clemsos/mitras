#!/usr/bin/env python
#coding=utf-8


from urllib2 import URLError
import time

from log import logger
from crawler import UserCrawler, SearchCrawler 
from fetcher import CnFetcher

def crawlUsers(uids=[]):

    fetcher = CnFetcher()
    fetcher.login()

    connection_error = False
    # print uids
    while len(uids) > 0 or connection_error:
        print "id processed"
        if not connection_error:
            uid = uids.pop()
        try:
            crawler = UserCrawler(uid, fetcher)
            crawler.run()
            connection_error = False
        except URLError, e:
            logger.exception(e)
            connection_error = True
            time.sleep(10)

def crawlSearch(words=[]):

    fetcher = CnFetcher()
    fetcher.login()

    connection_error = False
    # print uids
    while len(words) > 0 or connection_error:
        print "word processed"
        if not connection_error:
            word = words.pop()
        try:
            crawler = SearchCrawler(word, fetcher)
            crawler.run()
            connection_error = False
        except URLError, e:
            logger.exception(e)
            connection_error = True
            time.sleep(10)

    pass

if __name__ == "__main__":
    import argparse
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

    parser = argparse.ArgumentParser('Task to crawl sina weibo.')
    parser.add_argument('uids', metavar="uids", type=str, nargs="*",
                        help="uids to crawl")
    args = parser.parse_args()

    uids = args.uids
    # print uids
    # crawlUsers(uids)
    crawlSearch(uids)