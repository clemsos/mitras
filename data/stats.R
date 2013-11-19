# install.packages("tm")
# install.packages("RMongo")
# get data from mongo
library(RMongo)
db <- mongoDbConnect('protomemes')
print("connected to db")
print(dbShowCollections(db))

# query <- dbGetQuery(mg1, 'test', "{'AGE': {'$lt': 10}, 'LIQ': {'$gte': 0.1}, 'IND5A': {'$ne': 1}}")
query <- dbGetQuery(db, "week1", "")
# data <- query[c('users','txt','desc', 'tweets')]
txt <- query[c('txt')]
summary(txt)

library(tm)
# Prepare Data
# http://www.statmethods.net/advstats/cluster.html
# mydata <- na.omit(data) # listwise deletion of missing
# mydata <- scale(data) # standardize variables
corpus <- Corpus(VectorSource(txt))
dtm <- DocumentTermMatrix(corpus, control = list(weighting = weightTfIdf))