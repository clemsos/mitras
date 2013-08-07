#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pprint
from flask import Flask, request
import json


app = Flask(__name__)

# Import ENV
MITRAS_SPIDER_HOST = os.getenv('MITRAS_SPIDER_HOST', "127.0.0.1")
MITRAS_SPIDER_PORT = os.getenv('MITRAS_SPIDER_PORT', 5000)
MITRAS_ENV = os.getenv('MITRAS_ENV', 'development')

# setup right server
server="http://"+MITRAS_SPIDER_HOST+":"+str(MITRAS_SPIDER_PORT)
# app.config["SERVER_NAME"]=server

# API Web Server
@app.route('/tencent/callback', methods=['GET'])
def tencent_callback():

    code = request.args.get('code')
    openid = request.args.get('openid')
    openkey = request.args.get('openkey')
    state = request.args.get('state')

    # parse to json
    data= {
        "code": code,
        "openid" : openid,
        "openkey" : openkey,
        "state" : state
    }

    return json.dumps(data)


if __name__ == '__main__':
    app.run(debug=True)
