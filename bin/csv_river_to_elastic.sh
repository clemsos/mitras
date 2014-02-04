#!/bin/bash

# curl -XDELETE 'localhost:9200/_river/csv/'

# curl -XPUT localhost:9200/_river/csv/_meta -d '
# {
#   "type": "csv",
#   "csv_file": {
#     "folder": "/home/clemsos/Dev/mitras/data/",
#     "filename_mask": ".*\\.csv$",
#     "poll": "5m",
#     "fields": [
#       "mid",
#       "retweeted_status_mid",
#       "uid",
#       "retweeted_uid",
#       "source",
#       "image",
#       "text",
#       "geo",
#       "created_at",
#       "deleted_last_seen",
#       "permission_denied"
#     ],
#     "field_separator": ",",
#     "escape_character" : ";",
#     "quote_character" : "§"
#   },
#   "index": {
#     "index": "weiboscope",
#     "type": "tweet",
#     "bulk_size": 1000,
#     "bulk_threshold": 10
#   }
# }
# '