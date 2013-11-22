#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from time import time
# from matplotlib import pyplot

import numpy as np
from pylab import *
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.ticker as ticker

import datetime
import random
import time

from test_helpers import TestHelpers
helpers=TestHelpers()
# helpers.add_relative_path()

data=helpers.load_tweets("week1",100)

print "%d tweets loaded " % len(data)
print data[len(data)-1]
dates=[]
values={}

# create data
for tweet in data:
    t=tweet["created_at"]
    
    # TODO : explore this strange +1 hour fix
    d=datetime.datetime.strptime(t, "%Y-%m-%d %H:%M:%S") #+ datetime.timedelta(hours=1)

    day = datetime.datetime(d.year,d.month,d.day)
    i=day.strftime("%s")

    # collect values 
    if day not in dates :
        dates.append(day)
        values[i]=0    
    
    values[i]+=1

print len(dates)
print len(values)
print dates
print values

# parse data
x=dates
y=[values[v] for v in values]


########################################
# VARIABLES 

w=len(x) # width of the canvas
h=len(y) # height of the canvas

bar_color='#CCCCCC'
bar_width=.35

images_path="/home/clemsos/Dev/mitras/out/"
filename="tweet_volume"

########################################
# DRAW BAR GRAPH

def get_bar_graph(x,y):
    # Create a figure with size 6 x 6 inches.
    fig = plt.figure(figsize=(w,h))

    # Create a canvas and add the figure to it.
    canvas = FigureCanvas(fig)

    # bar plot for volume of
    bars = fig.add_subplot(111)

    # Display Grid
    bars.grid(True,linestyle='-',color='0.75')

    # Display Bars
    bars.bar(x, y, facecolor=bar_color, 
           align='center', ecolor='black')

    # This sets the ticks on the x axis to be exactly where we put the center of the bars.
    # bars.set_xticks(x)

    # Create a y label
    bars.set_ylabel('Counts')

    # Create a title, in italics
    bars.set_title('Volume of tweets, by day',fontstyle='italic')

    # Generate the Scatter Plot.
    # bars.scatter(x,y,s=20,color='tomato');

    # Auto-adjust and beautify the labels
    fig.autofmt_xdate()

    # Show us everything
    plt.show()

    # Save the generated Scatter Plot to a PNG file.
    fn=images_path+filename
    canvas.print_figure(fn,dpi=200)
    fig.savefig(fn+".pdf")
