import pylab
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.cluster.vq import kmeans,vq
from scipy.spatial.distance import pdist, squareform
from matplotlib import pyplot


query={}
protomemes= list(data.find(query).limit(protomemes_count))

print "%d protomemes obtained." % len(protomemes)
print "Processing data..."
print 

print '#'*40
print "Step 1 : Compute all vectors from protomemes"

##################################################################
# Text similarity (TF-IDF)
#

print '-'*40
print "Vectorizing tweets text"
print 
corpus=vectorize_text(protomemes)
text_matrix=tdidf(corpus)

##################################################################
# Diffusion similarity
# 

print '-'*40
print 'Vectorizing diffusion using RT/mentions users list'
print 

diffusion=[]
for proto in protomemes:
    diffusion.append(proto["users"])

dictionary=create_dictionary(diffusion)
vector_diffusion_corpus=get_frequency_vectors(diffusion,dictionary)
diffusion_matrix=create_matrix_from_vectors(vector_diffusion_corpus)


##################################################################
# Binary tweets
#

print '-'*40
print "Vectorizing tweets ids"
print

binary_tweets=[]
for proto in protomemes:
    binary_tweets.append(proto["tweets"])

tweet_dic=create_dictionary(binary_tweets)
tweet_corpus=get_frequency_vectors(binary_tweets,tweet_dic)
tweets_matrix=create_matrix_from_vectors(tweet_corpus)

##################################################################
# User similarity
# TODO : add all ids of user to protomemes (should be mined in prepare.py)
#
print '-'*40
print "TODO : Tweet simple similarity "
print 


##################################################################
# STEP 2 
# Compute similarities
#

# sims={}

print '#'*40
print
print "Step 2 : Compute cosine similarities based on corpus"
print " text_matrix - n_samples: %d, n_features: %d "%text_matrix.shape
print " tweets_matrix - n_samples: %d, n_features: %d "%tweets_matrix.shape
print " diffusion_matrix - n_samples: %d, n_features: %d "%diffusion_matrix.shape
print

text_sim=[cosine_similarity(pm, text_matrix)[0] for pm in text_matrix]
diffusion_sim=[cosine_similarity(pm, diffusion_matrix)[0] for pm in diffusion_matrix]
tweets_sim= [cosine_similarity(pm, tweets_matrix) for pm in tweets_matrix]

# BUG : tweet_sim not working
# print tweets_sim 

for p in diffusion_sim:
    print p
# print len(text_sim)
##################################################################
# STEP 3
# Combine and plot similarities
#

# TODO : add error if matrix size is different
print '#'*40
print "Step 3 : Combine similarities from the corpus"
print 
print "All records should be equal size"
print "text_sim",len(text_sim)
print "diffusion_sim",len(diffusion_sim)
print "tweets_sim",len(tweets_sim)
print

# linear combination of similarity measures,
print "Starting linear combination of similarity measures,"
wt = 0.0
wc = 0.7 
wu = 0.1
wd = 0.2

if wt+wc+wu+wd != 1:
    # TODO : throw error here
    print "ERROR : scale factors sum should equals 1"

# TODO add missing parameters
# print np.array(text_sim).shape
# print np.array(diffusion_sim).shape
combi=wc*np.array(text_sim) +wd*np.array(diffusion_sim)
# print combi.shape
# combi=wt*text_sim +wc*tweets_sim +wd*diffusion_sim #+wu*users_matrix

# print combi
# Compute clusters
# TODO : change method to "average"
clusters=linkage(combi, method='average')
print clusters.shape

#use vq() to get as assignment for each obs.
assignment,cdist = vq(clusters,clusters)
pyplot.scatter(clusters[:,0], clusters[:,1], c=assignment)
pyplot.show()