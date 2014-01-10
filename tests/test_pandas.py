import pandas as pd
import numpy as np
from time import time

from test_helpers import TestHelpers
helpers=TestHelpers()
helpers.add_relative_path()

import lib.tweetminer as minetweet
from lib.nlp import NLPMiner

path="/home/clemsos/Dev/mitras/"
file_path=path+"data/datazip/week10.csv"

# init 
# nlp=NLPMiner()
t0=time()

csvfile=pd.read_csv(file_path, iterator=True, chunksize=1000)
errors=0


# Reference different types of corpus
types=["txt","diffusion","tweets","users"]

hashtrain=[]
for i,df in enumerate(csvfile):
    # if i==100 : break
    print i

    # order by date
    df.reindex(index=df["created_at"])
    mentions,urls,hashtags,clean=[],[],[],[]

    for j,t in enumerate(df.text.values):
        try : # prevent empty value to break thread
            a,b,c,d=minetweet.extract_tweet_entities(t)
        except TypeError:
            a,b,c,d=[],[],[],[]
        mentions.append(a[0:5]),urls.append(b[0:5]),hashtags.append(c[0:5]),clean.append(d[0:5])
        
        # create training set
        for h in c:
            # print h,df.mid[j]
            hashtrain.append((h,df.mid[j]))

    try :
        types = [(mentions, "mentions"),
            (urls,"urls"),
            (hashtags,"hashtags")
            # (clean,"clean")
            ]

        # 
        for t in types:
            dfa=pd.DataFrame(t[0])
            col_names=[]
            for c in dfa.columns:
                col_names.append(t[1]+"_"+str(c))
            dfa.columns=col_names
            # print col_names
            dfa["mid"]=df["mid"]
            df=pd.merge(df,dfa)

        # print df
        df.to_csv(path+"tests/data/sample.csv")

    except AssertionError:
        print df
        errors+=1

# http://gehrcke.de/2013/07/data-analysis-with-pandas-enjoy-the-awesome/
# http://blog.yhathq.com/posts/predict-weather-with-kaggle-twitter-emoticons-pandas.html
 
train_set=pd.DataFrame(hashtrain)
train_set.columns=["hashtag","mid"]
train_set.save(path+"tests/data/df_hashtags_week1.csv")
# print train_set.groupby("hashtag").groups

print 
print "%d errors"%errors
print "done in %.3fs"%(time()-t0) 
# chunk=1000 - done in 144.438s

