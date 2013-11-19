#!/usr/bin/env python
# -*- coding: utf-8 -*-

if __name__ == '__main__' and __package__ is None:
    from test_helpers import TestHelpers
    helpers=TestHelpers()
    helpers.add_relative_path()

from lib.mongo import MongoDB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans #, MiniBatchKMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale
# from sklearn.metrics.pairwise import cosine_similarity
# from sklearn import metrics
import numpy as np
import pylab as pl

from time import time
import logging


# Display progress logs on stdout
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

# Variables # SETTINGS
collection="week1"  
proto_count=0 # number of protomemes to extract. Use zero to process all
nbRecords=5000

# Connect to Mongo
db=MongoDB("weibodata").db
data=db[collection]
tweets_count=data.count()
print 10*"-"
print str(tweets_count)+" tweets in the db"


###############################################################################
# Load data

print "Loading tweets from db..."
_type="dico"
query={_type: {"$not": {"$size": 0} } }
tweets=data.find(query).limit(nbRecords)

# print "Loaded "+str(len(tweets))+" tweets."

corpus=[]
STOP_TWEETS=["转发微博","轉發微博","分享图片"]

for t in list(tweets):
    dico=' '.join(x for x in t["dico"]) # TODO : if x not in STOP_TWEETS
    # print dico
    corpus.append(dico)

print "%d tweets in corpus" % len(corpus)
# print "%d categories" % len(dataset.target_names)
print

# labels = dataset.target
# true_k = np.unique(labels).shape[0]
true_k= 10

###############################################################################
# Create training set

print "Extracting features from the training dataset using a sparse vectorizer"
t0 = time()

tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)

print "done in %fs" % (time() - t0)
print "n_samples: %d, n_features: %d" % tfidf_matrix.shape
print

# print cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)

###############################################################################
# Do the actual clustering

# if opts.minibatch:
#     km = MiniBatchKMeans(k=true_k, init='k-means++', n_init=1,
#                          init_size=1000,
#                          batch_size=1000, verbose=1)
# else:

# km = KMeans(n_clusters=true_k, init='random', max_iter=100, n_init=1, verbose=1)
# print "Clustering sparse data with %s" % km
# t0 = time()
# km.fit(tfidf_matrix)
# print "done in %0.3fs" % (time() - t0)

# print km.labels_

# print "Homogeneity: %0.3f" % metrics.homogeneity_score(labels, km.labels_)
# print "Completeness: %0.3f" % metrics.completeness_score(labels, km.labels_)
# print "V-measure: %0.3f" % metrics.v_measure_score(labels, km.labels_)
# print "Adjusted Rand-Index: %.3f" % \
#     metrics.adjusted_rand_score(labels, km.labels_)
# print "Silhouette Coefficient: %0.3f" % metrics.silhouette_score(
#     X, labels, sample_size=1000)

print

###############################################################################
# Visualize the results on PCA-reduced data
n_digits=10
reduced_data = PCA(n_components=2).fit_transform(tfidf_matrix.toarray())
kmeans = KMeans(init='k-means++', n_clusters=n_digits, n_init=10)
kmeans.fit(reduced_data)

# Step size of the mesh. Decrease to increase the quality of the VQ.
h = 1     # point in the mesh [x_min, m_max]x[y_min, y_max].

# Plot the decision boundary. For that, we will assign a color to each
x_min, x_max = reduced_data[:, 0].min() + 1, reduced_data[:, 0].max() - 1
y_min, y_max = reduced_data[:, 1].min() + 1, reduced_data[:, 1].max() - 1
xx, yy = np.meshgrid(np.arange(x_max,x_min, h), np.arange(y_max,y_min, h))

print x_min,x_max,y_min,y_max
print xx,yy
print np.arange(3,7,2)
print np.arange(x_max,x_min)
print np.arange(y_max,y_min)

# Obtain labels for each point in mesh. Use last trained model.
Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

# Put the result into a color plot
Z = Z.reshape(xx.shape)
pl.figure(1)
pl.clf()
print xx.min(), xx.max(), yy.min(), yy.max()
pl.imshow(Z, interpolation='nearest',
          extent=(xx.min(), xx.max(), yy.min(), yy.max()),
          cmap=pl.cm.Paired,
          aspect='auto', origin='lower')

pl.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)
# Plot the centroids as a white X
centroids = kmeans.cluster_centers_
pl.scatter(centroids[:, 0], centroids[:, 1],
           marker='x', s=169, linewidths=3,
           color='w', zorder=10)
pl.title('K-means clustering on tweets dataset (PCA-reduced data)\n'
         'Centroids are marked with white cross')
pl.xlim(x_min, x_max)
pl.ylim(y_min, y_max)
pl.xticks(())
pl.yticks(())
pl.show()