import os

# scan all downloaded files
# raw_csv_folder=os.path.dirname(os.path.abspath(__file__)) +"/147.8.142.179/datazip/"
raw_csv_folder="/home/clemsos/Dev/mitras/data" +"/datazip/"
print raw_csv_folder
csvfiles = [ os.path.join(raw_csv_folder,f) for f in os.listdir(raw_csv_folder) if os.path.isfile(os.path.join(raw_csv_folder,f)) ]
print csvfiles

# for csv_file in data_files:
    # extract_and_store_tweets(csv_file,nlp, minetweet)
