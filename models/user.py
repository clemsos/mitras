#!/usr/bin/env python
# -*- coding: utf-8 -*-

from minimongo import Model, Index, configure
import json

# Mongo db
configure(host="localhost", port=27017)
db_name="tweets"

class User(Model):

    class Meta:
        # Here, we specify the database and collection names.
        # A connection to your DB is automatically created.
        database = db_name
        collection = "weibousers"

        # Now, we programatically declare what indices we want.
        # The arguments to the Index constructor are identical to
        # the args to pymongo"s ensure_index function.
        # TODO : add indexes 
        indices = (
            Index("uid"),
            Index("province")
        )

        def __init__(self):
            pass