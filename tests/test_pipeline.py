#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gensim import corpora, models, similarities,interfaces
from scipy import sparse
import numpy as np
from time import time
from scipy.cluster.hierarchy import linkage, dendrogram, leaves_list
import matplotlib.pyplot as plt
import fastcluster

from test_helpers import TestHelpers
helpers=TestHelpers()
helpers.add_relative_path()
from lib.protomemes import get_protomemes


proto_count=1000

# keywords have been extracted and stopwords removed.
print
print "WORKFLOW step by step"
print '#'*30
print

tstart=time()

data=get_protomemes(None,proto_count)
print "Data contains %d records"%len(data)

tweets=[]
diffusion=[]
users=[]
txt=[]

for proto in data:
    tweets.append(proto["value"]["tweets"])
    diffusion.append(proto["value"]["diffusion"])
    users.append(proto["value"]["users"])
    txt.append(proto["value"]["txt"].split())

to_vectorize=(tweets,diffusion,users,txt)
# print to_vectorize

# STEP 1 : Compile corpus and dictionary
print "STEP 1 : Index and vectorize"
print '-'*10


# create dictionary (index of each element)
for i,t in enumerate(to_vectorize):
    dictionary = corpora.Dictionary(t)
    dictionary.save('/tmp/'+str(i)+'.dict') # store the dictionary, for future reference
    print "Create a dictionary, an index of all unique values: %s"%type(dictionary)

    # compile corpus (vectors number of times each elements appears)
    raw_corpus = [dictionary.doc2bow(x) for x in t]
    print "Then convert convert tokenized documents to vectors: %s"% type(raw_corpus)
    corpora.MmCorpus.serialize('/tmp/'+str(i)+'.mm', raw_corpus) # store to disk
    print "Save the vectorized corpus as a .mm file"
    print

# STEP 2 : similarity between corpuses
print "STEP 2 : Transform and compute similarity between corpuses"
print '-'*10
t0=time()
for i,t in enumerate(to_vectorize):

    dictionary = corpora.Dictionary.load('/tmp/'+str(i)+'.dict')
    print "Load our dictionary : %s"% type(dictionary)

    corpus = corpora.MmCorpus('/tmp/'+str(i)+'.mm')
    print "Load our vector corpus : %s "% type(corpus) 

    # Train the TF-IDF model
    tfidf = models.TfidfModel(corpus) # step 1 -- initialize a model
    print "Initialize our TF-IDF transformation tool : %s"%type(tfidf)

    # corpus tf-idf
    corpus_tfidf = tfidf[corpus]
    print "Convert our vectors corpus to TF-IDF space : %s"%type(corpus_tfidf)

    print "Save the tranformed corpus"
    corpus_tfidf.save('/tmp/'+str(i)+'.trans')
    
    print
print "Done in %.3fs"%(time()-t0)
print

# STEP 3 : Create similarity index for all documents
print "STEP 3 : Create similarity matrix of all files"
print '-'*10
# index = similarities.MatrixSimilarity(corpus)
t0=time()
for i,t in enumerate(to_vectorize):

    dictionary = corpora.Dictionary.load('/tmp/'+str(i)+'.dict')
    print "Load our dictionary : %s"% type(dictionary)

    num_features=len(dictionary)
    print "Get the number of features :%d"%num_features

    print "Load the tranformed corpus"
    corpus=interfaces.TransformedCorpus.load('/tmp/'+str(i)+'.trans')

    index = similarities.Similarity('/tmp/'+str(i)+'.sims', corpus,num_features)
    print "Compute similarities from the transformed corpus : %s"%type(index)

    print "Save the similarity index"
    index.save('/tmp/'+str(i)+'.sims')
    print index
    print
print "Done in %.3fs"%(time()-t0)
print 
# STEP 4 : get similarities
print "STEP 4 : Getting similarities using training corpus"
print '-'*10

# streaming scenario
print 'Loop through each documents to see similarities'
t0=time()
print "Load the trained corpus"
print 

trained=[]
for i,t in enumerate(to_vectorize):
    
    # load training corpus
    corpus = corpora.MmCorpus('/tmp/'+str(i)+'.mm')
    print "Load vector corpus : %s "% type(corpus) 

    print "Load similarities index : %s "% type(corpus)     
    index = similarities.Similarity.load('/tmp/'+str(i)+'.sims')
    trained.append((corpus,index))
print 

# straeming scenario
combined_matrix=np.zeros([len(data),len(data)])

print 'Streaming scenario : one document at a time'
print "Computing combined similarity for all documents..."
for j in range(0,len(data)):
    # print "New document"

    combined_row = np.zeros([len(data)])

    for trained_set in trained :
        # print trained_set
        corpus= trained_set[0]
        index = trained_set[1]
        combined_row+=index[corpus[j]]

    combined_matrix[j]=combined_row
print 
print "Combined Matrix processed : (x: %d, y: %d)" % combined_matrix.shape
print "Done in %.3fs"%(time()-t0)
print 
# get similarity values
# sims = index[corpus]
# print "Get a similarity matrix  all documents in the corpus %s"% type(sims)

# sims_sparse= sparse.csr_matrix(sims)
# print "Convert it to scipy sparse row optimized matrix %s"%type(sims_sparse)

# STEP 5 : linkage
print "STEP 5 : compute clusters w average linkage algorithm"
print '-'*10
t0=time()
# linkage_matrix=linkage(combined_matrix, method='average') # very slow : O(n³)

# compute using fastcluster from Stanford O(n²)
# http://math.stanford.edu/~muellner/fastcluster.html
linkage_matrix=fastcluster.linkage(combined_matrix, method='average', metric='euclidean', preserve_input=True)

print " clusters: n_samples: %d, n_features: %d" % linkage_matrix.shape
print "Done in %.3fs"%(time()-t0)

# STEP 6 : plot / visualize
print "STEP 6 : plot / visualize"
print "Creating dendogram..."
dendrogram(linkage_matrix)
print "Finished in %.3fs"%(time()-tstart)



# plt.show() 

print 
print 
