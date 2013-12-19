#!/usr/bin/env python
# -*- coding: utf-8 -*-

from test_helpers import TestHelpers
helpers=TestHelpers()
helpers.add_relative_path()

from lib.mongo import MongoDB
from lib.geo import geocode
import ner
import json

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

from bottle import route, run, template, get, debug
from geojson import MultiPoint
from collections import Counter
# for tagger to work, we need to launch Stanford NER Java socket server 
tagger = ner.SocketNER(host='localhost', port=1234)

# Connect to Mongo
collection="memes"
memes_count = 20

db=MongoDB("weibodata").db
data=db[collection]
query = { "name" : "tmpioT57L"}
memes = list(data.find(query).limit(memes_count))
print len(memes)

path="/home/clemsos/Dev/mitras/data"

def get_geo_entities_list(_tweets):
    GPE=[]
    for t in _tweets:
        # prepare Chinese seg for ENR
        seg_str =""
        for word in t["dico"]:
            seg_str += word.encode('utf-8')+" "
        # print seg_str

        # get all entities 
        tags= tagger.get_entities(seg_str)
        # print tags
        for t in tags: 
            if t == "GPE" :#or t=="GPE":
                GPE.append(tags[t][0].encode('utf-8'))
    return GPE

def geocode_entities(_entities):
    places=[]
    places_occurences=Counter(_places)
    # print repr(places_occurences)
    print "%d unique places"%len(places_occurences)

    for p in places_occurences:
        print "--"*10
        print p
        try:
            place=p
            try :
                geoinfo=geocode(place)
                # print geoinfo
                geodata=(place,places_occurences[place],geoinfo)
                print geodata 
                places.append(geodata)
                print place
            except :
                pass

        except UnicodeDecodeError:
            print 'not valid'
            pass
    return places

def convert_geocoded_entities_to_geojson(_geocoded_entities):
    data=[]
    for p in _geocoded_entities:
        # place={}
        # place["name"]=p[0]
        # place["count"]=p[1]
        # place["geo"]={ "name":p[2][0], "latitude":p[2][1][0], "longitude":p[2][1][1] }

        place = (p[2][1][1],p[2][1][0])
        data.append(place)
    print type( data)
    return MultiPoint(data)

def get_geo_tag_as_geojson(_tweets):
    geotag=[ (float(t["geo"][6:-1].split(" ")[0]),float(t["geo"][6:-1].split(" ")[1])) for t in _tweets if t["geo"] !=""]
    # print type(geotag)
    return MultiPoint(geotag)


def test_get_data():
       places=[('\xe9\x9d\x9e\xe6\xb4\xb2', 1, (u'Africa', (-8.783195, 34.508523))), ('\xe9\x87\x91\xe6\xb2\x99\xe6\xb1\x9f', 1, (u'Yangtze River, China', (31.8469401, 120.8728615))), ('\xe5\x8d\x8e\xe5\x8d\x97\xe5\x9c\xb0\xe5\x8c\xba', 1, (u'China, Fujian, Fuzhou, Changle, \u90d1\u534e\u5357', (25.933843, 119.578345))), ('\xe7\x8f\xa0\xe4\xb8\x89\xe8\xa7\x92', 1, (u'Zhujiang River Estuary', (22.3574779, 113.7156809))), ('\xe6\xbe\x8e\xe6\xb9\x96 \xe4\xb8\x83\xe7\xbe\x8e \xe5\xb2\x9b', 1, (u'Daisho Island, Qimei Township, Penghu County, Taiwan 883', (23.2077778, 119.4311111))), ('\xe6\xac\xa7\xe8\x83\xa1\xe5\xb2\x9b', 2, (u'O\u2018ahu, Hawaii, USA', (21.4389123, -158.0000565))), ('\xe8\xa5\xbf\xe6\x98\x8c', 1, (u'Xichang, Liangshan, Sichuan, China', (27.894504, 102.264449))), ('\xe4\xb8\x9c \xe4\xb8\xad\xe8\xa1\x97', 1, (u'Dong Zhong Jie, Middle Street Shangquan, Dadong, Shenyang, China, 110000', (41.80284899999999, 123.470442))), ('\xe4\xba\x9a\xe6\xb4\xb2', 2, (u'Asia', (34.047863, 100.6196553))), ('\xe4\xb8\x89\xe8\xa7\x92\xe6\xb4\xb2', 2, (u'Delta, BC, Canada', (49.12, -122.99))), ('\xe7\x8e\xaf\xe5\xb2\x9b\xe8\xb7\xaf', 1, (u'Roundabout South Road, Siming, Xiamen, Fujian, China', (24.4318044, 118.1431777))), ('\xe6\xac\xa7\xe6\xb4\xb2', 2, (u'Europe', (54.5259614, 15.2551187))), ('\xe9\x98\xbf\xe5\xb0\x94\xe5\x8d\x91\xe6\x96\xaf\xe5\xb1\xb1', 4, (u'Alps', (46.5288067, 10.0794644)))]
       return places

def test_workflow():
    # get places
    tmp_places=[]
    with open(path+"/viz_test/LOC_ioT57L.txt", "r") as f:
        for line in f.readlines():
            place=line[:-1]
            tmp_places.append(place)
    print "%d places quoted in the corpus "%len(tmp_places)

    places=generate_geo_json()
    with open(path+"/out/geomeme.json", "w") as f:
        jsondata=json.dumps(places)
        f.write(jsondata)


for meme in memes:
    print get_geo_tag_as_geojson(meme["tweets"])


# miller projection
map = Basemap(projection='mill',lon_0=180)
# plot coastlines, draw label meridians and parallels.
map.drawcoastlines()
map.drawparallels(np.arange(-90,90,30),labels=[1,0,0,0])
map.drawmeridians(np.arange(map.lonmin,map.lonmax+30,60),labels=[0,0,0,1])
# fill continents 'coral' (with zorder=0), color wet areas 'aqua'
map.drawmapboundary(fill_color='aqua')
map.fillcontinents(color='coral',lake_color='aqua')
# shade the night areas, with alpha transparency so the
# map shows through. Use current time in UTC.
date = datetime.utcnow()
CS=map.nightshade(date)
plt.title('Day/Night Map for %s (UTC)' % date.strftime("%d %b %Y %H:%M:%S"))
plt.show()

# data=test_get_data()
# geojson=convert_geocoded_entities_to_geojson(data)

@route('/')
def index():
    return 'index'

@route('/entities.json')
def get_geodata():
    data = generate_data()
    # print data
    # return json.dumps(data, ensure_ascii=False)
    return data

@route('/geotag.json')
def get_geotag():
    pass

# run(host='localhost', port=8080)



# for meme in memes:
#     gpe=get_geo_entities_list(meme["tweets"])
#     for place in gpe:
#         print place

# tags_json = tagger.json_entities(seg_text)
# print tags_json