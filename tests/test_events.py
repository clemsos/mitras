#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Parse event list from WISE challenge and get dates 
'''
import urllib2
import urlparse

event_path="/home/clemsos/Dev/mitras/data/events_WISE.txt"


opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

with open(event_path, "r") as f:
    
    links = [line[len("Wikipedia Linkage: "):-1] for line in f if line.startswith('Wikipedia')]

    # print links

    for url in links:
        # print url
        pagename = urlparse.urlparse(url).path[len("/wiki/"):]
        
        api_url= 'http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&rvsection=0&titles='+pagename+'&format=xml'
        print api_url


    # infile = opener.open('http://en.wikipedia.org/w/index.php?title=Albert_Einstein&printable=yes')
    # page = infile.read()

            