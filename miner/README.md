# Detect memes

We aim at detecting memes from a social media dataset

## Protomemes
In a recent paper, E. Ferrara from Indiana U proposes a meme clustering algorithm based on the concept of protomeme [1]. We propose here a continuation and a slightly different implementation

### About protomemes
**Protomeme** is an abbreviation of "prototype meme". It refers to a meme which is under construction. The term "protomeme" was first used by Liane Gabora in 1997 [2]


Here protomemes are minimum meaningful units contained in tweets :

* hastag
* urls
* mentions/RT
* text

### Clustering 
After building the general set of protomemes vectors, we can compute their cosine similiarity to build clusters. We can compute different aspects :

* txt_similarity : TF-IDF vectors 
* tweets_similarity : hashtags/urls vectors
* user_similarity : users vectors 
* spread_similarity : directed graph of the conversation
* geo_spread_similarity : coordinates (from Weibo geo lat,lon)
* geo_similarity : geo (from NER entities)
* topic_similarity : keywords (from NER entities)
* people_similarity : people (from NER entities)


## Algorithm

Get Tweets
for each tweet :
	Extract entities regex (RT, @, #, http://)
	Extract NLP 
		keywords
		NER
	Compute Vectors (protomemes)
		from NLP
			keywords TF-IDF
			geo entities TF-IDF
			topic TF-IDF
		from social graph









## Ref

[1] http://www.emilio.ferrara.name/wp-content/uploads/2013/08/079_0108.pdf
[2] Gabora, Liane M. (1997) The Origin and Evolution of Culture and Creativity - Journal of Memetics: Evolutionary Models of Information Transmission, 1(1).








