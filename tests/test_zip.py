import os, zipfile
import pandas as pd

data_path="/home/clemsos/Dev/mitras/data/datazip/"

for path, subdirs, files in os.walk(data_path):
     for filename in files:
        try:
            # mypath=os.path.split(path)[1]
            if filename[-3:] == "zip" and filename[:4] == "week":
                # fin=('<img src="'+ f + '" />').decode('utf-8')
                # data.append({"path":fin})
                zip_path=path+ filename
                csvname=filename.split(".")[0]+".csv"
                with zipfile.ZipFile(zip_path) as z:
                    f = z.open(csvname)
                    csvfile=pd.read_csv(f, iterator=True, chunksize=1000)
                    print "#"*20
                    for i,df in enumerate(csvfile):
                        if i==10 : break
                        print i
                        # print df

        except UnicodeDecodeError:
            pass
            print "ERROR"

'''
'''