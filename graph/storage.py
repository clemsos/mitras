#!/usr/bin/env python
# -*- coding: utf-8 -*-

from py2neo import neo4j, node, rel
graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")

# create node