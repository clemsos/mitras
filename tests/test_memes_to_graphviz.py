#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

'''
from test_helpers import TestHelpers
helpers=TestHelpers()
helpers.add_relative_path()
from lib.memes import *

from os import listdir
from os.path import isfile, join

path="/home/clemsos/Dev/mitras/data/out"

t0=time()

meme_list =get_meme_list()

for meme_name in get_meme_list():
    meme_to_gv_file(meme_name,path)    


gv_files = [ f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f)) and os.path.splitext(f)[1] == ".gv" ]

for gv_file in gv_files:
    png_file=os.path.splitext(gv_file)[0]+".png"

    print "creating graph file from %s"%gv_file
    command = "sfdp -Gbgcolor=black -Ncolor=white -Ecolor=white -Nwidth=0.05  -Nheight=0.05 -Nfixedsize=true -Nlabel='' -Earrowsize=0.4 -Gsize=75 -Gratio=fill -Tpng " + path+"/"+gv_file + " > " + path+"/graphviz/"+png_file
    
    os.system(command)
    print "graph saved as %s"%png_file
    

print " done in %fs" % (time() - t0)