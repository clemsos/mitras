#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import route, run, template, get, debug, static_file
import os, time
import base64
import json
import csv


data_types=["json","csv"]
data_rep="/home/clemsos/Dev/mitras/results"

def get_meme_list():

    meme_list_file=data_rep+"/2012_sina-weibo-memes_list.csv"

    # parse data
    with open(meme_list_file, 'rb') as csv_memelist:
        memelist=csv.reader(csv_memelist)
        keys,memes=[],[]
        for i,meme in enumerate(memelist):        
            if i==0: keys=meme
            temp_mm={}
            for j,col in enumerate(meme):
                temp_mm[keys[j]]=col
            memes.append(temp_mm)

    return memes

def generate_data():
    data=[]
    memes=get_meme_list()

    for path, subdirs, files in os.walk(data_rep):     
        meme_name=os.path.split(path)[1]
        for m in memes :
            if m["safename"]==meme_name:
                data.append(m)

        # print "meme"
        # print len(meme)
        # print meme

    return {"data":  data}

# @get('/<filename:re:.*\.(jpg|png|gif|ico)>')
# def images(filename):
#     f=os.path.join(os.path.split(os.path.split(filename)[0])[1],os.path.split(filename)[1])+"/ui"
#     return static_file(f, root=file_rep)

# serve static
@route('/<filename:re:.*\.(css|js|csv|json|jpg|png|gif|ico)>')
def server_static(filename):
    return static_file(filename, root=os.getcwd()+"/ui")

@route('/')
def index():  
    return template('ui/index')

@route('/memes.json')
def images_getallitems():
    data = generate_data()
    # print data
    # return json.dumps(data, ensure_ascii=False)
    return data

run(host='localhost', port=8080,reloader=True)