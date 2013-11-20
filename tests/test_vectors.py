#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import tfidf

# table = tfidf.tfidf()

# table.addDocument("tweet1", ["", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel"])
# table.addDocument("tweet2", ["alpha", "bravo", "charlie", "india", "juliet", "kilo"])
# table.addDocument("tweet3", ["kilo", "lima", "mike", "november"])

# print table.similarities (["alpha", "bravo", "charlie"])

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

documents = (
"The sky is blue",
"The sky is grey",
"The sun is bright",
"The sun in the sky is bright",
"We can see the shining sun, the bright sun",
"the sky is green",
"the blue is green"
)


tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
print tfidf_matrix.shape

print cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)
