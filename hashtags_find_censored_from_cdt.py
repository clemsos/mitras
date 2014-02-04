import csv
import os

root_path="/home/clemsos/Dev/mitras/"
data_path=root_path+"data/"

# get censored
censored_list_path=data_path+"SensitiveSinaWeiboSearchTerms.csv"
censored_words=[]
with open(censored_list_path, 'rb') as cs_file:
    csv_censor=csv.reader(cs_file)
    censored_words=[word[0] for word in csv_censor]

# get hashtags
hashtags_path=root_path+"top_hashtags.csv"
hashtags=[]
with open(hashtags_path, 'rb') as cs_file:
    csv_hash=csv.reader(cs_file)
    hashtags=[word[0] for word in csv_hash]

censored_hashtags=[h for h in hashtags if h in censored_words]
print censored_hashtags

for censored_word in censored_hashtags:
    print censored_word