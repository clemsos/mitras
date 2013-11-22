#!/usr/bin/env python

"""
The simplest TF-IDF library imaginable.

Add your documents as two-element lists `[docname, [list_of_words_in_the_document]]` with `addDocument(docname, list_of_words)`. Get a list of all the `[docname, similarity_score]` pairs relative to a document by calling `similarities([list_of_words])`.

See the README for a usage example.

from https://github.com/hrs/python-tf-idf

"""

import sys
import os

class tfidf:
    def __init__(self):
        self.weighted = False
        self.documents = []
        self.corpus_dict = {}

    def addDocument(self, doc_name, list_of_words):
        # building a dictionary
        doc_dict = {}
        print "new doc -------"
        for w in list_of_words:
            doc_dict[w] = doc_dict.get(w, 0.) + 1.0
            self.corpus_dict[w] = self.corpus_dict.get(w, 0.0) + 1.0
            print w,doc_dict[w],self.corpus_dict[w]

        # print "normalizing the dictionary"
        length = float(len(list_of_words))
        for  k,key in doc_dict.iteritems():
            doc_dict[k] = doc_dict[k] / length

        # add the normalized document to the corpus
        self.documents.append([doc_name, doc_dict])

    def similarities(self, list_of_words):
        """Returns a list of all the [docname, similarity_score] pairs relative to a list of words."""

        print 'similarities #######################'
        # building the query dictionary
        query_dict = {}
        for w in list_of_words:
            query_dict[w] = query_dict.get(w, 0.0) + 1.0
            print w, query_dict[w]

        # normalizing the query
        length = float(len(list_of_words))
        for k in query_dict:
            query_dict[k] = query_dict[k] / length

        # computing the list of similarities
        sims = []
        for doc in self.documents:
            score = 0.0
            
            print "------------doc"
            # print doc[1]

            doc_dict = doc[1]
            for k in query_dict:

                print k,query_dict[k]
                # check if keyword is in the doc
                if doc_dict.has_key(k):
                    score += (query_dict[k] / self.corpus_dict[k]) + (doc_dict[k] / self.corpus_dict[k])
                print score
            sims.append([doc[0], score])

        return sims