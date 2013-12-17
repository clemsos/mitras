#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''

'''
from test_helpers import TestHelpers
helpers=TestHelpers()
helpers.add_relative_path()
from lib.visualizer import get_graph_csv_filenames

import csv

path="/home/clemsos/Dev/mitras/data/out"

def process_all(_path):
    graph_filenames= get_graph_csv_filenames(_path)

    for i,d in enumerate(graph_filenames):
        # t0=time()    
        # if i==1 : break
        node_file=_path+"/"+graph_filenames[d][0]
        edge_file=_path+"/"+graph_filenames[d][1]

        print node_file, edge_file

node_path="/home/clemsos/Dev/mitras/data/out/tmpG5y2n9_nodes.csv"
edge_path="/home/clemsos/Dev/mitras/data/out/tmpG5y2n9_edges.csv"

