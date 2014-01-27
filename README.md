# Mitras : Mining memes

	**Work in Progress : not ready to use yet**

Mitras is a data analysis project. Its purpose is to detect and visualize memes from a large corpus of tweets from Sina Weibo. It has been developed by Clément Renaud for his phD research on memes on Sina Weibo.

## Thanks to :
* The Weiboscope team in HKU
* Mingli Yuan
* 




## Workflow : Overview 

1. Download dataset (HKU Weiboscope corpus, 16GB)
2. Parse data properly (csv to MongoDB)
3. Extract and vectorize knowledgable entities (map-reduce protomemes)
4. Produce stats to catch a grasp on the dataset (plot, time series...)
5. Compute similarities within corpus (text,diffusion,users,tweets)
6. Detect clusters and identify important memes (k-means)
7. Create meme dataset and extract geo-entities (NER,map-reduce,Neo4J)
9. Visualize identified memes (gephi, node, d3.js)

It includes detection of memes (clustering), localization in Chinese (NLP), geo-entities (NER, geotag) and visualization for classification.

## Detailed Workflow 

### Data : tweet corpus 
To create this project we will use the data provided by the project Weiboscope from HKU University, JMSC - [link](http://147.8.142.179/datazip/). The dataset contains sample data from 52 weeks of 2012 from more than 350,000 Chinese microbloggers who have more than 1,000 followers (Fu, Chan, Chau, 2013 ; Fu, Chau, 2013).

Note : this data has been anonymized

**Data Set Statistics:**

	* Number of weibo messages: 226841122
	* Number of deleted messages: 10865955
	* Number of censored ('Permission Denied') messages: 86083
	* Number of unique weibo users: 14387628
	* 57 files, 18G

### Extract Protomemes 
To detect memes in this large corpus, we design a clustering algorithm using the concept of protomeme as described in [Ferrara, 2013](http://www.emilio.ferrara.name/2013/08/01/clustering-memes-in-social-media/). Protomemes are minimum units contained in tweets :

* hashtags
* urls
* mentions/RT
* text


### Compute Similarities
For each protomemes, we compute the (cosine) similiarity on different vector spaces as follow :

* txt_similarity : tweet text using TF-IDF 
* tweets_similarity : hashtags/urls only
* user_similarity : users (binary) vectors 
* diffusion_similarity : graph of the conversation as (binary) vector

Those different similarities values are combined into a single using weighted index :

	wt = 0.0 , wc = 0.7 , wu = 0.1 , wd = 0.2
	combined_index = wc*txt_sim + wd*diff_sim + wt*tweets_sim + wu*users_sim


### Clustering
Using the combined index, we use k-means and MAX algorithm to identify clusters within the protomemes set and define memes.


### Memes Semantic Parsing
For each memes, we collect all tweets and we extract named entities using Stanford NER

* Segmentation using Guokr's [segmentation tool](https://github.com/guokr/gkseg) and training [corpus](https://github.com/guokr/corpus)
* NER using Stanford Parser


### Visualization
The visualization engine will show multi-layered navigation with different dimension for different similarity. We need to have pre-computed set of data to create powerful visualization.

Viz engine will be developed in NodeJS, HTML5, ProcessingJS, d3.js, MapBox - using WebGL.

## Usage

### Install

	sudo apt-get install python-pip
	pip install bson jieba pymongo

	# Install optimized calculus tools : numpy / scipy 
	cd setup 
	bash install_blas.sh 

	# mongo models
	git clone https://github.com/slacy/minimongo.git && cd minimongo 
	python setup.py install

	# Stanford NER
	git clone https://github.com/dat/pyner
    python setup.py install

To install Tilemill on Debian : 
	
	https://www.mapbox.com/tilemill/docs/source/
	https://gist.github.com/springmeyer/2164897

### Download & Prepare Data

	# to download the data
	bash bin/get_raw_data.sh

	#  Downloaded: 57 files, 18G in 6h 42m 3s (803 KB/s)

	# move the files to the data folder
	mv 147.8.142.179/datazip data/datazip
	rm -R 147.8.142.179

	# remove zip files
	ls data/datazip/*zip | xargs -i rm {} 
