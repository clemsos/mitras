#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, webbrowser

from ConfigParser import ConfigParser
from qqweibo import API, JSONParser
from qqweibo import OAuth2_0_Handler as AuthHandler


class TencentSpider:

    def __init__(self):

        config = ConfigParser()
        config.read( os.path.join(os.path.abspath(".") + os.sep +  'settings.py') )

        # Setup Sina Weibo credentials
        self.API_KEY = config.get('tencent', 'key')
        self.API_SECRET = config.get('tencent', 'secret')
        self.openid = config.get('tencent', 'openid')
        self.access_token = config.get('tencent', 'access_token')
        self.refresh_token = config.get('tencent', 'refresh_token')
        
        # setup ENV
        MITRAS_SPIDER_HOST = os.getenv('MITRAS_SPIDER_HOST', "127.0.0.1")
        MITRAS_SPIDER_PORT = os.getenv('MITRAS_SPIDER_PORT', 5000)

        # callback URL to spider server
        self.CALLBACK_URL = "http://"+MITRAS_SPIDER_HOST +":"+ str(MITRAS_SPIDER_PORT)+'/tencent/callback'


    def auth_to_weibo(self):

        # Create API Client
        self.auth = AuthHandler(self.API_KEY, self.API_SECRET, self.CALLBACK_URL)

        # TODO : implement logic to renew tokens
        # if expired:
            # spider.create_token()
        # else:
            # self.set_token()

        self.set_token()
        return self.auth
        

    def get_api(self, parser):
        # print parser
        self.api = API(self.auth, parser)
        print 'logged in to Tencent Weibo'
        return self.api


    def create_token(self): 
        ## use get_authorization_url if you haven't got a token
        url = self.auth.get_authorization_url()
        print ('Opening {:s} in your browser...'.format(url))
        webbrowser.open_new(url)

        # TODO : remove interactive creation
        verifier = input('Your CODE: ').strip()
        token = self.auth.get_access_token(verifier)
        return token

    def set_token(self):
        # self.auth.setToken(self.access_token, self.openid)
        # now you have a workable api
        self.auth.set_token(self.openid,self.access_token,self.refresh_token)
        return self.auth

    def save_token(self, token):
        return token

    def test_api(self):
        # or use `api = API(auth)`
        print ("User Infomation:")
        I = self.api.user.info()                     # or api.me()
        data = I['data']

        print I

    def remaining_hits(self):
        self.api