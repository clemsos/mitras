# Mitras

Mitras is a SNA prototype developed for my phD thesis

###  Purpose 
The general idea is to see how individuals and communities react after a meme spread.

### Hypothesis 
The communities and individuals that reacts to a single meme are already largely similar.
Memes are not increasing serendipity but reinforce links between similar groups and individuals.

### Methodology
So to test this hypothesis, we need to observe :
- Social graph evolution on meme path
- Similarity between groups and individuals 

### Technological stack

EXTRACTION
* Data crawling using [cola](https://github.com/chineking/cola) framework
* Storage in [mongoDB](http://mongodb.org)

MINING
* Job & tasks queues and  with [Redis](http://redis.org)
* Chinese NLP : Guokr's [segmentation tool](https://github.com/guokr/gkseg) and [corpus](https://github.com/guokr/corpus)
* Mining using Javascript
* Relationship storage using [Neo4j](http://neo4j.org)

FRONTEND
* Server with [Node/Express.js](http://expressjs.org) through [WebSockets](http://socket.io)
* UI with [AngularJS](angularjs.org)
* Visualization with [Gephi](http://gephi.org/), [d3.js](http://d3js.org) and [Processing JS](http://processingjs.org/)


## Algorithm

### Data Collection

#### 1. Constitute meme text corpus from Weibo*
manual collection of 1-10 seed posts on weibo (chrome plugin)

#### 2. Constitute users corpus from Weibo*
crawl profiles+timelines of all users mentionned in posts corpus

### Mining

#### 3. Extract social relationship corpus *
dont take friend/follow into account : it is static, very noisy signal and not very useful.
also we need to be able to see relationships evolution in time > it is not possible to find creation time of friend/follow relationships from weibo API. Only dynamic extraction from timeline : messages exchanged= relationships, no visible exchange=no relationship so we can see evolution of relationships between users.
each @ / comment creates a relationship between 2 users 

#### 4. Extract semantic corpus
for each user, extract entities (places and topics) from his timeline 

#### 5. Extract semantic relationships corpus  
Define similarity between users by comparing most-used entities
The semantic similarity between two users is calculated as follow : 
- similar posts/reposts in timeline
- similar entities (topics & places) 

### Visualization

#### 6. Refine with Gephi
As everything is stored using Neo4j, it will be easy to visualize with Gephi to get a general sense of graphe evolution. Then we can define important steps in evoluiton of the meme and how it reflects in the social graph.

#### 7. Publish 
To be able to browse similarities, we will need to color code based on communities or users entities, so it will take an interactive interface.
This can be done with d3 and a clean data API for Neo4J


So we can have some results and conclusions and test this hypothesis.

