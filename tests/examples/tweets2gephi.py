#!/usr/bin/python

#T2G: Twitter-to-Gephi converter, Python edition v 0.3 (07/09/13)
#This script converts user mentions in tweets into a format capable of being imported into Gephi (https://gephi.org/), a social network visualization platform. It was written and tested under Python 2.7.5, so YMMV under different installations. 
#To use it, begin by creating an input CSV file consisting of two columns: the first (leftmost) containing the usernames of the tweet authors, and the second containing their tweets. Each author username must have a corresponding tweet next to it. Move this file into the working directory of your choice (if using the interpreter this is usually the file where your Python binary lives). Change the 'extmode' variable on line 16 before execution if desired. After executing T2G, type the name of your input file exactly (including the extension) and it should do its job. The output file should import into Gephi as a directed graph in which ties extend from authors to mentioned users.
#Please report all bugs and unexpected behavior to deen@dfreelon.org.
#Changelog:
#07/09/13 -- Added options to extract retweets only, non-RTs only, and exclude singletons
#06/20/13 -- Fixed a bug that caused an error whenever two @ symbols appeared adjacent to one another.

import csv
import re
import types

#Extraction mode -- change the value of the variable below to 1, 2, 3, or 4 to change which network edges T2G extracts. Default is 1
extmode = 1
#1=do not differentiate between retweets and non-retweets, include singletons
#2=do not differentiate between retweets and non-retweets, exclude singletons
#3=retweets only, exclude singletons
#4=non-retweets (mentions) only, exclude singletons

file = raw_input('Please enter the name of a properly-formatted CSV file: ')
t_list = []

with open(file, 'rb') as f: #opens the CSV file, which must be properly formatted, and inserts all content into t_list
    reader = csv.reader(f)
    for row in reader:
        t_list.append(row)

if extmode == 2:
    g_src = [t[0].lower() for t in t_list if t[1].find('@')>-1] #fills in the list g_src with the names of tweeting users
    g_tmp = [' ' + t[1] + ' ' for t in t_list if t[1].find('@')>-1] #adds 1 space to beginning and end of each tweet
elif extmode == 3:
    g_src = [t[0].lower() for t in t_list if t[1].find('RT @')>-1]
    g_tmp = [' ' + t[1] + ' ' for t in t_list if t[1].find('RT @')>-1] 
elif extmode == 4:
    g_src = [t[0].lower() for t in t_list if t[1].find('RT @')==-1 and t[1].find('@')>-1]
    g_tmp = [' ' + t[1] + ' ' for t in t_list if t[1].find('RT @')==-1 and t[1].find('@')>-1] 
else:
    g_src = [t[0].lower() for t in t_list] 
    g_tmp = [' ' + t[1] + ' ' for t in t_list] 
del t_list #to free up memory
g_tmp = [t.split('@') for t in g_tmp] #splits each tweet along @s
g_trg = [[t[:re.search('[^A-Za-z0-9_]',t).start()].lower().strip() for t in chunk if type(re.search('[^A-Za-z0-9_]',t)) is not types.NoneType] for chunk in g_tmp] #strips out everything after the @ sign and trailing colons, leaving (hopefully) a list of lists of usernames
for line in g_trg:
    if len(line) > 1 and line[0] == '': #removes blank entries from lines mentioning at least one name
        del line[0]

final = []
i = 0

if extmode == 3:
    for list in g_trg: #creates final output list
        final.append(g_src[i] + ',' + list[0] + "\n")
        i+=1
else:
    for list in g_trg: #creates final output list
        for name in list:
            final.append(g_src[i] + ',' + name + "\n")
        i+=1

outfile = file + '_gephiready_python.csv'
with open(outfile,'wb') as out: #writes the final output to CSV
    for row in final:
        out.write(row)

print 'Conversion complete. Your export file is "' + outfile + '".'