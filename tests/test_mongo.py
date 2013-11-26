# test_mongo.py
'''
Test write / read on mongoDB
'''

from lib.mongo import MongoDB
import datetime
import json
from minimongo import Model, Index


class MongoTest(unittest.TestCase):

    def setUp(self):
        self.data = [{"author": "Mike",
         "text": "My first blog post!",
         "tags": ["mongodb", "python", "pymongo"],
         "date": datetime.datetime.utcnow()
         }]
    
    def test_connection(self):
        # db=mongoDB('test')
        # db.save_data(data, "my_collec")
    
    def test_minimongo(self):
        # Create & save an object, and return a local in-memory copy of it:
        foo = Foo({"x": 1, "y": 2}).save()

        # Find that object again, loading it into memory:
        foo = Foo.collection.find_one({"x": 1})
        print foo

        # Change a field value, and save it back to the DB.
        foo.other = "some data"
        foo.save()