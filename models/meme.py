from minimongo import Model, Index, configure
import json

# mongo db
configure(host="localhost", port=27017)
db_name="weibodata"

class Meme(Model):

    class Meta:
        # Here, we specify the database and collection names.
        # A connection to your DB is automatically created.
        database = db_name
        collection = "memes"

        # Now, we programatically declare what indices we want.
        # The arguments to the Index constructor are identical to
        # the args to pymongo"s ensure_index function.
        # TODO : add indexes 
        # indices = (
        #     # Index("mid"),
        #     # Index("mid")
        # )

    def __init__(self):
        print "a new meme !"
        pass