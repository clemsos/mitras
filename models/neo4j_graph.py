#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from py2neo import neo4j, node, rel
from bulbs.config import DEBUG
from bulbs.neo4jserver import Graph, Config, NEO4J_URI
from message import Message, IsRetweet # models
from datetime import datetime

# setup 
config = Config(NEO4J_URI, "james", "secret")
g = Graph(config)
# g.config.set_logger(DEBUG)

# g.add_proxy("message", Message)
g.add_proxy("tweet", Message)
g.add_proxy("isRT", IsRetweet)

# create node
m1= g.tweet.create(text="salut",created_at=datetime.now())
m2= g.tweet.create(text="re-salut",created_at=datetime.now())

# nodes = g.tweet.index.lookup(text="salut")

# create edge
rt=g.isRT.create(m2,m1)

# Connect to neo4j
# graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/"
