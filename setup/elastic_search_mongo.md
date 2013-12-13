PINSTALL

    wget 
    dpkg -i elasticsearch*
    bin/plugin --install com.github.richardwilly98.elasticsearch/elasticsearch-river-mongodb/1.7.3


MONGO config

https://blog.zenithar.org/articles/2013-10-19-persistence-mongodb-indexation-elasticsearch.html

    $ mongo
    MongoDB shell version: 2.4.7
    connecting to: test
    > cfg = { "_id" : "rs0", "version" : 1, "members" : [ { "_id" : 0, "host" : "localhost:27017" } ] }
    {
        "_id" : "rs0",
        "version" : 1,
        "members" : [
            {
                "_id" : 0,
                "host" : "localhost:27017"
            }
        ]
    }
    > rs.initiate(cfg)
    {
        "info" : "Config now saved locally.  Should come online in about a minute.",
        "ok" : 1
    }
    > 

Config ElasticSearch

    $ curl -XPUT "localhost:9200/_river/tweets/_meta" -d '
    {
      "type": "mongodb",
      "mongodb": {
        "servers": [
          { "host": "127.0.0.1", "port": 27017 }
        ],
        "options": { "secondary_read_preference": true },
        "db": "weibodata",
        "collection": "tweets"
      },
      "index": {
        "name": "hashtags",
        "type": "txt"
      }
    }'