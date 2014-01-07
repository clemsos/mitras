import pandas as pd
import numpy as np

from test_helpers import TestHelpers
helpers=TestHelpers()
helpers.add_relative_path()

import lib.tweetminer as minetweet
from lib.nlp import NLPMiner

path="/home/clemsos/Dev/mitras/data"
file_path=path+"/datazip/week10.csv"

# init 
# nlp=NLPMiner()

csvfile=pd.read_csv(file_path, iterator=True, chunksize=1000)

for i,df in enumerate(csvfile):
    if i==1 : break
    print df.describe()
    df.reindex(index=df["created_at"])
    # print df.head()
    # print df

    text = df[df.text.notnull()].text.values
    print len(text)
    # df["mentions"],df["urls"],df["hashtags"],df["clean"]=minetweet.extract_tweet_entities(df["text"])
    mentions=[]
    urls=[]
    hashtags=[]
    clean=[]
    for t in text:
        # print t
        a,b,c,d=minetweet.extract_tweet_entities(t)
        mentions.append(a)
        urls.append(b)
        hashtags.append(c)
        clean.append(d)

    print len(mentions),len(urls),len(hashtags),len(clean)
    df["mentions"],df["urls"],df["hashtags"],df["clean"]=mentions,urls,hashtags,clean

    