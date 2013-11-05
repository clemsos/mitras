# test_mongo.py
'''
Test write / read on mongoDB
'''

# from models.mongo_db import mongoDB
# import datetime
# import json

# data = [{"author": "Mike",
#          "text": "My first blog post!",
#          "tags": ["mongodb", "python", "pymongo"],
#          "date": datetime.datetime.utcnow()
#          }]


# db=mongoDB('test')
# db.save_data(data, "my_collec")

from minimongo import Model, Index


# Create & save an object, and return a local in-memory copy of it:
foo = Foo({"x": 1, "y": 2}).save()

# Find that object again, loading it into memory:
foo = Foo.collection.find_one({"x": 1})
print foo

# Change a field value, and save it back to the DB.
foo.other = "some data"
foo.save()