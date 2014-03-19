# NLP

##  Gkseg

Segmentation Algorithm for Chinese Language

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


