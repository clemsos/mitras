#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns


root_path="/home/clemsos/Dev/mitras/out/hashtags/"
data_path=root_path+"data/"

# sns.set_color_palette("deep", desat=.6)
# mpl.rc("figure", figsize=(8, 4))


df=pd.read_csv(root_path+"hashtags_stats.csv")
# df=df.drop("label",1).astype("float64")
# sns.lmplot("tweets","conversation",df)
# df=df.drop(df.index[:3]).head()

plt.scatter(df["tweets"], df["conversation"], s=df["label"])
plt.show()