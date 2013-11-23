# Mitras

Mitras is a SNA prototype developed for my phD thesis
	
	Work in Progress : not ready to use yet

## Aims
This tool analyse data from Sina Weibo with following goals:

* identify memes from randomly sampled data (using clustering /unsepervised learning) 
* extract entities from Chinese text using Stanford NER
* extract active social graph (conversational graph)
* visualize relationships between entities and memes


## Data

### Tweet corpus 
To create this project we will use the data provided by the project Weiboscope from HKU University - [link](http://147.8.142.179/datazip/). Note : this data has been anonymized

	# to download the data
	bash bin/get_raw_data.sh

	#  Downloaded: 57 files, 18G in 6h 42m 3s (803 KB/s)

	# move the files to the data folder
	mv 147.8.142.179/datazip data/datazip
	rm -R 147.8.142.179

	# remove zip files
	ls data/datazip/*zip | xargs -i rm {} 
	
	# Parse data and store tweets in MongoDB
	bash bin/prepare.py

	# in mySQL (some bugs)
	# bash data/data_csv_to_mysql.sh


## Mining memes

### Extract Protomemes 
To detect memes in this large corpus, we design a clustering algorithm using the concept of protomeme as described in [Ferrara, 2013](http://www.emilio.ferrara.name/2013/08/01/clustering-memes-in-social-media/). Protomemes are minimum units contained in tweets :

* hastag
* urls
* mentions/RT
* text

### Semantic Entities
For each tweet, we can also extract entities using Stanford NER

* Segmentation using Guokr's [segmentation tool](https://github.com/guokr/gkseg) and [corpus](https://github.com/guokr/corpus)
* NER using Stanford Parser

### Clustering 
After building the general set of protomemes vectors, we can compute their cosine similiarity to build clusters. We can compute different aspects :

* txt_similarity : TF-IDF vectors 
* tweets_similarity : hashtags/urls vectors 
* user_similarity : users vectors 
* conversation_similarity : directed graph of the conversation
* coord_similarity : coordinates (from Weibo geo lat,lon)
* geo_similarity : geo (from NER entities)
* topic_similarity : keywords (from NER entities)
* people_similarity : people (from NER entities)

## Computing clusters
Once we have computed those different clusters, we can observe different ways for messages to create clusters i.e. memes. By using different combinations and parameters, we can therefore study how different aspects of similarity between messages and users can influence the constitution of different memes.

## Visualization
The visualization engine will show multi-layered navigation with different dimension for different similarity. We need to have pre-computed set of data to create powerful visualization.

Viz engine will be developed in NodeJS, HTML5, ProcessingJS, d3.js, MapBox - using WebGL.
