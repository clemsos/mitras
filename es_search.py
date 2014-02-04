from pyelasticsearch import ElasticSearch


es = ElasticSearch('http://localhost:9200/')
es.refresh('weiboscope')

# es.get('weiboscope', 'tweet', 2)

es.search('*', index='weiboscope')

