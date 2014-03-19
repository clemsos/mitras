# Install and configure

To run those scripts, you will need some Python scientific libraries like : numpy / scipy, pandas, scikit-learn, etc. I strongly advice you use iPython to have the full stack and run step by step through the notebook for better comprehension of the workflows.

## Install basics

    sudo apt-get install python-pip
    pip install bson jieba pymongo

    # mongo models
    git clone https://github.com/slacy/minimongo.git && cd minimongo 
    python setup.py install

    # Stanford NER
    git clone https://github.com/dat/pyner
    python setup.py install

## Scipy / Numpy

Optimized BLAS Installation for numpy see this [post](http://williamjohnbert.com/2012/03/how-to-install-accelerated-blas-into-a-python-virtualenv/)

    #!/bin/bash
    workon [envname]
    pip uninstall numpy ## only if numpy is already installed
    pip uninstall scipy ## only if scipy is already installed
    export LAPACK=/usr/lib/liblapack.so
    export ATLAS=/usr/lib/libatlas.so
    export BLAS=/usr/lib/libblas.so
    pip install scipy numpy



## Pandas

[Pandas](http://pandas.pydata.org/) is a library to handle data frames in Python - like R does. Great also to deal with large files

### Install On Ubuntu

    sudo apt-get update
    sudo apt-get install python-setuptools
    sudo apt-get install python-dev
    # Download numpy-1.7.1.tar.gz from [Sourceforge](http://sourceforge.t/projects/numpy/files/NumPy/1.7.1/numpy-1.7.1.tar.gz/download)
    wget http://heanet.dl.sourceforge.net/project/numpy/NumPy/1.7.1/numpy-1.7.1.tar.gz
    tar zxvf numpy-1.7.1.tar.gz && cd numpy-1.7.1/
    sudo python setup.py install
    pip install pandas


## Chinese NLP : Gkseg

** Segmentation Algorithm for Chinese Language ** 

### Install

```
    git clone git://github.com/guokr/gkseg.git

    # add gkseg to Python Path
    cd gkseg
    pwd >> /usr/local/lib/python2.7/dist-packages/gkseg.pth

    # build wapiti
    cd gkseg/wapiti
    make

    # test the install
    cd ..
    python examples/async.py

```

### Get the corpus

    git clone https://github.com/guokr/corpus

## Name Entities Recognition (NER)

### Setup

Download [Stanford NER](http://nlp.stanford.edu/software/CRF-NER.shtml)  and [Chinese Classifiers Pack](http://nlp.stanford.edu/software/CRF-NER.shtml) from Standofrd website

Install Pyner from [Github rep](https://github.com/dat/pyner)

    git clone https://github.com/dat/pyner
    python setup.py install

### Launch NER server

    # Chinese
    bash ner-zh-server.sh
    
    # English
    bash ner-en-server.sh


## Neo4j

Relationships mining is operated directly from the timeline data, using quotes, RT.
The embed social graph contained in conversations is used instead of the follow/friend relationships.


### Install on Debian/Ubuntu 

Check this [Gist](https://gist.github.com/quinn/1307556) 

### Tips / Best Practices for Neo4j
Some important tips from http://aseemk.com/talks/neo4j-with-nodejs

* Use specific names bcz it is your onyl way to make requests in Cypher
* Cache numbers AFAP bcz requests on big grpahs are expensive
* Use event nodes to capture history and changes in the graph
* Store multi-relatiosnhsips as node is better
* If you have "category" and "thing", better to have 2 nodes
* THE Supernode problem : use index to avoid nodes w too many relationships

### Neo4j Models

Using [Bulbs](http://bulbflow.com/) for Python

about bulbs

* http://stackoverflow.com/questions/14281251/bulbflow-difference-between-neo4jserver-graph-and-neo4jserver-neo4jclient/15358024#15358024

* Save a dict as node property : http://stackoverflow.com/questions/19033357/bulbflow-how-to-save-list-dictionary-as-property/19125386#19125386

* Data-intensive use with Gremlin : http://stackoverflow.com/questions/16759606/is-there-a-equivalent-to-commit-in-bulbs-framework-for-neo4j/16764036#16764036

* importing large dataset in Neo4j :http://jexp.de/blog/2013/05/on-importing-data-in-neo4j-blog-series/

## Tilemill

Tilemill is a great tool to produce beautiful maps. It can be run as a nodejs server and therefore support live data updates through websockets for instance. 

### Install on Debian : 
    
    https://www.mapbox.com/tilemill/docs/source/
    https://gist.github.com/springmeyer/2164897