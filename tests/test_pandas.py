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
    # print df.head()
    # print df.describe()
    df.reindex(index=df["created_at"])
    df["mentions"],df["urls"],df["hashtags"],df["clean"]=minetweet.extract_tweet_entities(df["text"])
