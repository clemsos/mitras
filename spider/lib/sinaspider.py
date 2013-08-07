# -*- coding: utf-8 -*-
#/usr/bin/env python

import sys, os, urllib, urllib2, fnmatch
import csv, io
import fileinput
import getpass
import pickle
import datetime

from sina.weibo import APIClient # api from:http://michaelliao.github.com/sinaweibopy/

from helpers.http_helper import *
from helpers.retry import *

import storer.fileUtil as fileUtil
from rq import Queue, use_connection

try:
    import json
    from ConfigParser import ConfigParser
except ImportError:
    import simplejson as json

# setting sys encoding to utf-8
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


class SinaSpider:

    def __init__(self):

        config = ConfigParser()
        config.read( os.path.join(os.path.abspath(".") + os.sep +  'settings.py') )

        # Setup Sina Weibo credentials
        self.APP_KEY = config.get('sina', 'key')
        self.APP_SECRET = config.get('sina', 'secret')
        self.CALLBACK_URL = config.get('sina', 'callback')
        self.USERID = config.get('sina', 'username')       # 微博用户名                     
        self.USERPASSWD = config.get('sina', 'password')   # 用户密码

        # Setup tokens file path
        save_access_token_file  = 'access_token.txt'
        file_path = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + "sina" + os.path.sep
        self.ACCESS_TOKEN_FILE_PATH = file_path + save_access_token_file

    def auth_to_weibo(self):

        # Create API Client
        self.client = APIClient(app_key=self.APP_KEY, app_secret=self.APP_SECRET, redirect_uri=self.CALLBACK_URL)

        # Set user
        # TODO implement logic to check tokens expiration
        tokens  = [ tuple(line.split()) for line in open(self.ACCESS_TOKEN_FILE_PATH, 'r')]
        
        self.client.set_access_token(tokens[0][1],tokens[0][2])
        print "logged to Sina Weibo"

    def get_api(self):
        return self.client

    # OAUTH Tokens business logic
    def make_access_token(self,username, password):
        '''请求access token'''

        params = urllib.urlencode({'action':'submit','withOfficalFlag':'0','ticket':'','isLoginSina':'', \
            'response_type':'code', \
            'regCallback':'', \
            'redirect_uri':self.CALLBACK_URL, \
            'client_id':self.APP_KEY, \
            'state':'', \
            'from':'', \
            'userId':username, \
            'passwd':password, \
            })

        login_url = 'https://api.weibo.com/oauth2/authorize'

        url = self.client.get_authorize_url()
        content = urllib2.urlopen(url)
        if content:
            headers = { 'Referer' : url }
            request = urllib2.Request(login_url, params, headers)
            opener = get_opener(False)
            urllib2.install_opener(opener)
            try:
                f = opener.open(request)
                print f.headers.headers
                return_callback_url = f.geturl
                print f.read()
            except urllib2.HTTPError, e:
                return_callback_url = e.geturl()
            # 取到返回的code
            code = return_callback_url.split('=')[1]
        #得到token
        token = self.client.request_access_token(code)
        self.save_access_token(username,token)

    def save_access_token(self,username,token):
        '''将access token保存到本地'''

        print token
        exists = False
        done = False
        # f = open(self.access_token_file_path, 'r+')
        # for line in f:

        for line in fileinput.input(self.ACCESS_TOKEN_FILE_PATH, inplace=1):
            if username in line:
                exists = True
                print( username+' '+token['access_token']+' ' + str(token['expires_in']) )
            else:
                continue
        # done =True

        # print exists
        # print done
        
        # if exists == False:
        #     with open(self.access_token_file_path, 'a') as f:
        #         f.write(username+' '+token['access_token']+' ' + str(token['expires_in']))
        #         f.close()

    @retry(1)
    def apply_access_token(self,username, password):
        '''从本地读取及设置access token'''
        try:
            #loop to each line
            for line in open(access_token_file_path, 'r').readlines():
                #check if the username has already been added
                if username in line:
                    token =line.split()
                    
                    if len(token) != 3: #if size problem, make new one
                        self.make_access_token(username, password)
                        return False
                    
                    # 过期验证
                    usname, access_token, expires_in = token
                    try:
                        self.client.set_access_token(access_token, expires_in)
                    except StandardError, e:
                        if hasattr(e, 'error'): 
                            if e.error == 'expired_token':
                                # token过期重新生成
                                self.make_access_token(username, password)
                        else:
                            pass
                else:
                    pass
        except:
            self.make_access_token(username, password)
        
        return False

    # TODO : This function should accept an array (create multiple tokens)
    def create_new_tokens():
        self.apply_access_token(self.USERID,self.USERPASSWD)
        return ""

    # GET statuses/show : basic info on a post from API
    def getPost(self, uid):
        re = self.client.statuses__show(id=uid)
        return re

    # GET closest posts :
    def getPostsNearby(self, lat, lon, rang, count, page):
        re = self.client.place__nearby_timeline(lat=lat,long=lon,range=rang,count=count, page=page, sort=0) # sort=0 by time, sort=1 by closest post
        return re

