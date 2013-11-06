#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import MySQLdb
from datetime import datetime

# import miner.tweet as minetweet
# import miner.nlp as nlp
# import miner.geo as geo

from gensim import corpora, models, similarities

# MODELS
from bulbs.config import DEBUG
from bulbs.neo4jserver import Graph, Config, NEO4J_URI
from models.message_neo4j import Message, IsRetweet # models
from models.tweet import Tweet

# Learn machine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

######################## 
# SETTINGS
######################## 

# graph DB
graph_name="test"
graph_password="secret"
graph_host=NEO4J_URI

# ML
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


''' 
1. Prepare the Data 
-----------------------
 * Read CSV file
 * Extract all entities
 * Format properly
 * Store to MongoDB
'''

# see prepare.py

''' 
2. Create Protomemes
* process the data
* 
'''

# Request mongo


###################
# COMPUTE TF-IDF
##################

stop_tweets=["转发微博","轉發微博","分享图片"]

texts=[]

for t in tweets:
    doc=t.clean
    # prevent common tweets from being added
  
    if doc not in stop_tweets:

        # extract keywords
        dico=nlp.extract_dictionary(doc)
        
        # remove stopwords
        # TODO : remove blank space
        t.keywords=[w for w in dico if w.encode('utf-8') not in stoplist]
        if len(t.keywords) is not 0:
            texts.append(t.keywords)

print str(len(texts))+" textual documents processed"


# Create corpus
# TODO : optimize memory management :http://radimrehurek.com/gensim/tut1.html#corpus-streaming-one-document-at-a-time

# remove words that appear only once in the corpus
all_tokens = sum(texts, [])
tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
texts_ok = [[word for word in text if word not in tokens_once] for text in texts]

# create index dictionary for all terms
dictionary = corpora.Dictionary(texts_ok)
dictionary.save('/tmp/weibo.dict') # store the dictionary, for future reference
# print dictionary.token2id

# compute to vectors
corpus = [dictionary.doc2bow(t.keywords) for t in tweets]
corpora.MmCorpus.serialize('/tmp/weibo.mm', corpus) # store to disk, for later use
# print corpus

#initialize a model
tfidf = models.TfidfModel(corpus) # step 1 -- initialize a model
corpus_tfidf=tfidf[corpus] # step 2 -- use the model to transform vectors


# index.save('/tmp/deerwester.index')
# for doc in corpus_tfidf:
#     print doc






# tfidf_vectorizer = TfidfVectorizer()

# Use a custom pre-processing segmentation/tokenizer algorithm
# http://scikit-learn.org/dev/modules/feature_extraction.html#customizing-the-vectorizer-classes

# tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
# print tfidf_matrix.shape
# print cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)




###################
# CREATE GRAPH
##################

# NEO4J DB
config=Config(graph_host,graph_name,graph_password)
graph=Graph(config)
# g.config.set_logger(DEBUG)

# g.add_proxy("message", Message)
graph.add_proxy("tweet", Message)
graph.add_proxy("isRT", IsRetweet)

# Build Graph
def create_nodes():
    node_count=0
    for t in tweets:
        # BUG : fix CSV data import, should ignore ',' within quote marks (reproduce w sampleweibo.csv row 176)
        print t.txt
        if t.created_at is not "" and t.created_at[0] is "2":
            m1= graph.tweet.create(mid=t.mid,text=t.txt.encode('utf-8'),created_at=t.created_at)
            node_count+=1
            print t.mid+" - created in neo db"
    print "GRAPH - total node created   : "+str(node_count)

def create_edges():
    total_edges=0
    for t in tweets:    
        # print t.to_JSON()
        # build RT graph
        if t.retweetFromPostId:
            print ''
            print total_edges, t.mid, t.retweetFromPostId
            # print m1
            m1=graph.vertices.get_or_create('mid',t.mid)
            m2=graph.vertices.get_or_create('mid',t.retweetFromPostId)

            rt=graph.edges.create(m1,'isRT',m2)

            # graph.edges.create(m1,'isRT',m2)
            total_edges+=1
            
            # print m1
            # print m2
            
            # print "RT "+t.retweetFromPostId
            # print "RT @"+t.retweetFromUserId

        # build mention graph
        # for mention in mentions:
            # if mention[0] is "u" and "ukn" not in mention :
                # print "@"+mention

    print "GRAPH - total edges created   : "+str(total_edges)

# create_nodes()
# create_edges()
