#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
# import network x
import networkx as nx

from os import listdir
from os.path import isfile, join
import math
try:
    import matplotlib.pyplot as plt
except:
    raise
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
try:
    from networkx import graphviz_layout
    layout=nx.graphviz_layout
except ImportError:
    print "PyGraphviz not found; drawing with spring layout; will be slow."
    layout=nx.spring_layout

from test_helpers import TestHelpers
from time import time

helpers=TestHelpers()
helpers.add_relative_path()

from lib.visualizer import get_graph_csv_filenames, create_network_graph

def test_get_graph_data_from_csv_files(_path):
    mypath=_path+"/out"
    csvfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]

    data={}

    # parse all csv files
    print "%d csv files"% len(csvfiles)

    for f in csvfiles:
        if ".csv" in f :
            try: 
                data[f[3:-10]]
            except KeyError: 
                data[f[3:-10]] =["a","b"]

            if (f[10:-4]) == "nodes": 
                data[f[3:-10]][0]=f # data[f[3:-10]][0]=f
            else: 
                data[f[3:-10]][1]=f # data[f[3:-10]][1]=f

    print "%d edges/nodes couples"% len(data)

    return data

# create network graphs for each graph
def test_create_network_graph(_graph_filenames):
    for i,d in enumerate(_graph_filenames):
        t0=time()
        
        # if i==1 : break
        node_file=mypath+"/"+data[d][0]
        edge_file=mypath+"/"+data[d][1]
        # print(node_file,edge_file)

        if node_file[len(mypath)+3:-10] != edge_file[len(mypath)+3:-10] : raise ValueError
        
        name =node_file[len(mypath)+3:-10]

        # init
        w=12 # width of the canvas
        h=12 # height of the canvas

        # Create a figure with size 6 _x 6 inches.
        fig = plt.figure(figsize=(w,h))

        # Create a canvas and add the figure to it.
        canvas = FigureCanvas(fig)
        region=120 # for pylab 2x2 subplot layout
        plt.subplots_adjust(left=0,right=1,bottom=0,top=0.95,wspace=0.01,hspace=0.01)

        # start Graph
        G=nx.Graph()

        nodes=[]
        edges=[]

        # add node and edges to the graph
        with open(node_file, 'r') as f:
                next(f) # skip csv header
                data_csv = csv.reader(f)
                
                for row in data_csv: # one row at a time
                    nodes.append(row[0])
                    G.add_node(row[0])
                    # print(row[0])
        # print nodes

        with open(edge_file, 'r') as f:
                next(f) # skip csv header
                data_csv = csv.reader(f)
                
                for row in data_csv: # one row at a time
                    edges.append((row[0],row[1]))
                    # print row
                    # print (row[0],row[1])
                    try :
                        G.add_edge(nodes.index(row[0]),nodes.index(row[1]))
                    except ValueError:
                        pass


        # delete all unconnected nodes
        treshold_connections=5 # minimum number of connections for nodes to be kept 
        well_connected_graphs=[g for g in nx.connected_component_subgraphs(G) if len(g.nodes()) > treshold_connections]

        print " From %d nodes, we identified %d groups wher nodes have more than %d connections "%(len(G.nodes()), len(well_connected_graphs),treshold_connections)

        # re-init
        Gcc=nx.Graph()
        for g in well_connected_graphs: 
            G.subgraph(g)

        n=len(nodes)

        # p value at which giant component (of size log(n) nodes) is expected
        # p_giant=1.0/(n-1)

        # p value at which graph is expected to become completely connected
        # p_conn=math.log(n)/float(n)

        # G=nx.binomial_graph(n,p)
        

        # print(G.nodes())
        # pos=layout(Gcc)
        # pos=nx.spring_layout(Gcc, iterations=3)
        # repr( pos)

        # nx.draw_networkx_edges(Gcc,pos,
        #         with_labels=False,
        #         edge_color='r',
        #         width=6.0
        #         )

        # identify largest connected component
        # pos=layout(G0)
        
        # primary graph
        plt.subplot(region)
        plt.title("Principal shape / meme %s"%name)
        
        G0=well_connected_graphs[0]
        pos=nx.spring_layout(G0, iterations=3)
        nx.draw_networkx_edges(G0,pos,
                               with_labels=False,
                               edge_color='#E62E25',
                               alpha=0.5,
                               width=1.7
                            )
        nx.draw_networkx_nodes(G0,pos,
                               with_labels=False,
                               edge_color='#E62E25',
                               node_size=50,
                               node_shape="+",
                               alpha=0.5,
                               width=1.7
                            )

        # show other connected components
        region+=1
        plt.subplot(region)
        plt.title("Secondary shape")
        for Gi in well_connected_graphs[1:]:
           if len(Gi)>1:
            pos=layout(Gi)
            nx.draw_networkx_edges(Gi,pos,
                                     with_labels=False,
                                         edge_color='#4C66A4',
                                     alpha=0.3,
                                     width=1.5
                                     )
        # plt.subplot(region)
        # # print edges
        # # save file
        fn=mypath+"/"+name+".png"
        canvas.print_figure(fn,dpi=200)
        print "file saved as %s"%fn
        # plt.savefig("giant_component.png")
        # plt.show() # display
        
        print "done in %.3fs"%(time()-t0)


path="/home/clemsos/Dev/mitras/data"
tstart=time()

data = get_graph_csv_filenames(path)
print data
create_network_graph(data)

print "done in %.3fs"%(time()-tstart)