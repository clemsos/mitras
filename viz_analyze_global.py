#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv,os
import json
# from time import time
# import networkx as nx
# import pylab as plt
# from collections import Counter
# import community

results_path="/home/clemsos/Dev/mitras/results/"
meme_names=[ meme for meme in os.listdir(results_path) if meme[-3:] != "csv"]
meme_names=["biaoge"]

meme_names.sort()

t0=time()

for meme_name in meme_names: