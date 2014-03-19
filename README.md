# Mitras : Mining memes

Mitras is a set of scripts used to detect, analyse and visualize memes the Chinese microblog Sina Weibo. You will need the Weiboscope dataset prepared by HKU
It has been developed by Clément Renaud for his phD research.


## Mining workflow : 
The different workflows used in this research are documented in iPython notebook in the 
```/doc``` folder.

* ```es_*``` : plain-text search and mining with ElasticSearch and Kibana
* ```hashtags_*``` : build and analyze a corpus of all hashtags in the datasets
* ```pm_*``` : meme detection clustering algorithm using protomemes [(Ferrara, 2013)](http://www.emilio.ferrara.name/2013/08/01/clustering-memes-in-social-media/)

For visualisation, we use Matplotlib, d3js, Networkx and Gephi.

## Data : the Weiboscope  corpus 
To create this project we will use the data provided by the project Weiboscope from HKU University, JMSC - [link](http://147.8.142.179/datazip/). The dataset contains sample data from 52 weeks of 2012 from more than 350,000 Chinese microbloggers who have more than 1,000 followers (Fu, Chan, Chau, 2013 ; Fu, Chau, 2013).

Note : this data has been anonymized

**Data Set Statistics:**

    * Number of weibo messages: 226841122
    * Number of deleted messages: 10865955
    * Number of censored ('Permission Denied') messages: 86083
    * Number of unique weibo users: 14387628
    * 57 files, 18G

**Download & Prepare Data**

    # to download the data
    bash bin/get_raw_data.sh

    #  Downloaded: 57 files, 18G in 6h 42m 3s (803 KB/s)

    # move the files to the data folder
    mv 147.8.142.179/datazip data/datazip
    rm -R 147.8.142.179

    # remove zip files
    ls data/datazip/*zip | xargs -i rm {} 
