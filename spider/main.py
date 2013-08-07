#!/usr/bin/env python
import redis

import lib.tencentspider as TencentSpider
from qqweibo.utils import timestamp_to_str
from qqweibo import JSONParser

import lib.sinaspider as SinaSpider


import lib.server as SpiderServer
import lib.scheduler as SpiderScheduler


from pprint import pprint
import json


if __name__ == "__main__":

    # TENCENT WEIBO
    # tencent_spider = TencentSpider.TencentSpider()
    # tencent_auth = tencent_spider.auth_to_weibo()
    # tencent_api = tencent_spider.get_api("")

    # tencent_me = tencent_api.user.info("clemsos")
    # print tencent_me.name, tencent_me.nick, tencent_me.location

    # SINA WEIBO
    sina_spider = SinaSpider.SinaSpider()
    sina_auth = sina_spider.auth_to_weibo()
    sina_api = sina_spider.get_api()

    me = sina_api.users__show(screen_name="clemsos")
    print me["name"], me["screen_name"], me["city"]

    # TWITTER?
    


    # Start Server
    # spiderServer.run_server()
    
    # scheduler =SpiderScheduler.SpiderScheduler(spider)
    # weibo_session = auth_to_weibo()
    # redis = redis.Redis("localhost")
    # run_bot(weibo_session, redis, MITRAS_KEYWORDS)