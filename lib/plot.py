#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import datetime
import time
from utils import slugify
from scipy.cluster.hierarchy import dendrogram

def create_bar_graph(_x,_y,_title,_disp):

    print "Creating bar graph..."
    # VARIABLES 
    bar_color='#CCCCCC'
    bar_width=.35

    images_path="/home/clemsos/Dev/mitras/out/"

    w=len(_x) # width of the canvas
    h=len(_y) # height of the canvas

    # Create a figure with size 6 _x 6 inches.
    fig = plt.figure(figsize=(w,h))

    # Create a canvas and add the figure to it.
    canvas = FigureCanvas(fig)

    # bar plot for volume of
    bars = fig.add_subplot(111)

    # Display Grid
    bars.grid(True,linestyle='-',color='0.75')

    # Display Bars
    bars.bar(_x, _y, facecolor=bar_color, 
           align='center', ecolor='black')

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


def plot_sparcity():
    # should use matplotlib spy : http://matplotlib.org/examples/pylab_examples/spy_demos.html
    pass

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


# VIZ lib
# http://bokeh.pydata.org/