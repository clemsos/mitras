curl -XGET 'http://localhost:9200/weiboscope/tweet/1?pretty=true'


curl -XGET 'http://localhost:9200/weiboscope/tweet/_search?q=草泥马&pretty=true'

# number of censored posts 
curl -XGET 'http://localhost:9200/weiboscope/tweet/_search?pretty=true&search_type=count' -d '{
  "query": {
    "filtered": {
      "query": {
        "query_string": {
            "query": "permission_denied:exists"
         }
      },
      "filter": {
        "numeric_range": {
          "created_at": {
            "gte": "2012-02-05",
            "lte": "2012-04-20"
          }
        }
      }
    }
  }
}'


curl -XDELETE 'http://localhost:9200/weiboscope/tweet/_query' -d '
{
    "range" : {
        "date_time" : { "from" : "2012-01-01 00:00:01", "to" : "2012-02-03 01:59:59"}
    }
}'