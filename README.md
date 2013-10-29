# Mitras

Mitras is a SNA prototype developed for my phD thesis
	
	Work in Progress : not ready to use yet

## Aims
This tool analyse data from Sina Weibo with following goals:

* identify memes from randomly sampled data (using clustering /unsepervised learning) 
* extract entities from Chinese text using Stanford NER
* map relationships between entities and memes


## Data

### Tweet corpus 
To create this project we will use the data provided by the project Weiboscope from HKU University - [link](http://147.8.142.179/datazip/)

	# to download the data
	wget -r http://147.8.142.179/datazip/

Other data source could be crawled using the [cola](https://github.com/chineking/cola) framework 


### Meme corpus
Using clustering algorithm

### Semantic corpus
for each user, extract entities (places and topics) from his timeline 