# Social Graph

Relationships mining is operated directly from the timeline data, using quotes, RT.
The embed social graph contained in conversations is used instead of the follow/friend relationships.

## Neo4j

### Install on Ubuntu 

Check this [Gist](https://gist.github.com/quinn/1307556) 

### Tips / Best Practices for Neo4j
Some important tips from http://aseemk.com/talks/neo4j-with-nodejs

* Use specific names bcz it is your onyl way to make requests in Cypher
* Cache numbers AFAP bcz requests on big grpahs are expensive
* Use event nodes to capture history and changes in the graph
* Store multi-relatiosnhsips as node is better
* If you have "category" and "thing", better to have 2 nodes
* THE Supernode problem : use index to avoid nodes w too many relationships

### Modeling 

Using [Bulbs](http://bulbflow.com/) for Python

about bulbs

* http://stackoverflow.com/questions/14281251/bulbflow-difference-between-neo4jserver-graph-and-neo4jserver-neo4jclient/15358024#15358024

* Save a dict as node property : http://stackoverflow.com/questions/19033357/bulbflow-how-to-save-list-dictionary-as-property/19125386#19125386

* Data-intensive use with Gremlin : http://stackoverflow.com/questions/16759606/is-there-a-equivalent-to-commit-in-bulbs-framework-for-neo4j/16764036#16764036

* importing large dataset in Neo4j :http://jexp.de/blog/2013/05/on-importing-data-in-neo4j-blog-series/

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

