#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import datetime
import time
from utils import slugify
from scipy.cluster.hierarchy import dendrogram
import numpy as np

import networkx as nx

from os import listdir
from os.path import isfile, join
import math
import csv

from pytagcloud import create_tag_image,make_tags

try:
    from networkx import graphviz_layout
    layout=nx.graphviz_layout
except ImportError:
    print "PyGraphviz not found; drawing with spring layout; will be slow."
    layout=nx.spring_layout


# TODO : VIZ lib
# http://bokeh.pydata.org/


def create_bar_graph(_x,_y,_title,_disp):

    print "Creating bar graph..."
    # VARIABLES 
    bar_color='#2ca02c'


    images_path="/home/clemsos/Dev/mitras/out/"

    w=18 # width of the canvas
    h=15 # height of the canvas

    print min(_x), max(_x)

    bar_width= 0.026 #w/len(_x)
    print w, len(_x), bar_width

    # Create a figure with size 6 _x 6 inches.
    fig = plt.figure(figsize=(w,h))

    # Create a canvas and add the figure to it.
    canvas = FigureCanvas(fig)

    # bar plot for volume of
    bars = fig.add_subplot(111)

    # Display Bars
    bars.bar(_x, _y, width=bar_width, facecolor=bar_color, align='center', edgecolor="#74c476")

    # Display Grid
    bars.grid(True,linestyle='-',color='0.75')

    # TODO : set the axis below
    # Axis.set_axisbelow()

    # This sets the ticks on the x axis to be exactly where we put the center of the bars.
    # bars.set_xticks(_x)

    # Create a y label
    bars.set_ylabel('Counts')

    # Create a title, in italics
    bars.set_title(_title,fontstyle='italic')

    # Generate the Scatter Plot.
    # bars.scatter(_x,_y,s=20,color='tomato');

    # Auto-adjust and beautify the labels
    fig.autofmt_xdate()

    # Save the generated Scatter Plot to a PNG file.
    fn=images_path+slugify(_title)
    canvas.print_figure(fn,dpi=200)
    fig.savefig(fn+".pdf")
    
    print " graph file has been at %s.png"%fn
    print " graph file has been at %s.pdf"%fn

    # Show us everything
    if _disp is True :
        plt.show() 

def create_dendogram(_matrix,_title,_disp):

    print "Creating dendogram..."
    
    # VARIABLES 
    bar_color='#CCCCCC'
    bar_width=.35

    images_path="/home/clemsos/Dev/mitras/out/"

    w=12 # width of the canvas
    h=12 # height of the canvas

    # Create a figure with size 6 _x 6 inches.
    fig = plt.figure(figsize=(w,h))

    # Create a canvas and add the figure to it.
    canvas = FigureCanvas(fig)

    # bar plot for volume of
    tree = fig.add_subplot(111)

    # Display Grid
    tree.grid(True,linestyle='-',color='0.75')

    # Create a y label
    tree.set_ylabel('Counts')
        
    # Create a title, in italics
    tree.set_title(_title,fontstyle='italic')

    # Generate the Scatter Plot.
    # bars.scatter(_x,_y,s=20,color='tomato');
    augmented_dendrogram(_matrix,
                   color_threshold=1,
                   p=6,
                   truncate_mode='lastp',
                   show_leaf_counts=True,
                   )

    # Auto-adjust and beautify the labels
    # fig.autofmt_xdate()

    # Save the generated Scatter Plot to a PNG file.
    fn=images_path+slugify(_title)
    canvas.print_figure(fn,dpi=200)
    fig.savefig(fn+".pdf")
    
    print " graph file has been at %s.png"%fn
    print " graph file has been at %s.pdf"%fn

    # Show us everything
    if _disp is True :
        plt.show() 
    pass

def create_pie_chart(_fracs,_labels, _title,_disp):
    
    # make a square figure and axes
    print "Creating pie chart..."

    # VARIABLES 
    images_path="/home/clemsos/Dev/mitras/out/"

    w=8 # width of the canvas
    h=8 # height of the canvas

    # Create a figure with size 6 _x 6 inches.
    fig = plt.figure(figsize=(w,h))

    # Create a canvas and add the figure to it.
    canvas = FigureCanvas(fig)
    # ax = axes([0.1, 0.1, 0.8, 0.8])
    # explode=(0, 0.05, 0, 0)

    pie = fig.add_subplot(111)

    cmap = plt.cm.prism
    colors = cmap(np.random.random(len(_fracs)))

    pie.pie(_fracs, labels=_labels, labeldistance=1.05, autopct='%1.1f%%', shadow=False, colors=colors)

    pie.set_title(_title,fontstyle='italic')

    # Save the generated Scatter Plot to a PNG file.
    fn=images_path+slugify(_title)
    canvas.print_figure(fn,dpi=200)
    fig.savefig(fn+".pdf")
    
    print " graph file has been at %s.png"%fn
    print " graph file has been at %s.pdf"%fn

        # Show us everything
    if _disp is True :
        plt.show() 

def create_tag_cloud(_count, _name):
    tags = make_tags(_count, maxsize=150,colors=((59,76,76), (125,140,116), (217,175,95), (127,92,70), (51,36,35)))
    print tags
    create_tag_image(tags, _name, size=(900, 600), fontname="Chinese",background=(0, 0, 0),  )


def augmented_dendrogram(*args, **kwargs):
    ddata = dendrogram(*args, **kwargs)

    if not kwargs.get('no_plot', False):
        for i, d in zip(ddata['icoord'], ddata['dcoord']):
            x = 0.5 * sum(i[1:3])
            y = d[1]
            plt.plot(x, y, 'ro')
            plt.annotate("%.3g" % y, (x, y), xytext=(0, -8),
                         textcoords='offset points',
                         va='top', ha='center')
    return ddata

def plot_sparcity():
    # should use matplotlib spy : http://matplotlib.org/examples/pylab_examples/spy_demos.html
    pass

def get_graph_csv_filenames(_path):

    csvfiles = [ f for f in listdir(_path) if isfile(join(_path,f)) ]

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
# create network graphs for each graph
def create_network_graph(_path,_graph_filenames):
    for i,d in enumerate(_graph_filenames):
        # t0=time()
        
        # if i==1 : break
        node_file=_path+"/"+_graph_filenames[d][0]
        edge_file=_path+"/"+_graph_filenames[d][1]
        # print(node_file,edge_file)

        if node_file[len(_path)+3:-10] != edge_file[len(_path)+3:-10] : raise ValueError
        
        name =node_file[len(_path)+3:-10]

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
        fn=_path+"/"+name+".png"
        canvas.print_figure(fn,dpi=200)
        print "file saved as %s"%fn
        # plt.savefig("giant_component.png")
        # plt.show() # display
        
        # print "done in %.3fs"%(time()-t0)

