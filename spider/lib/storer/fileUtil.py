# -*- coding: utf-8 -*-

# fileUtil.py
# Write to file etc...

import os
import csv, json


def toFile(JSONOBJ, fileName, path, format):

    fn = fileName+"."+format
    filePath = os.path.join(path, fn)
    # print JSONOBJ

    if os.path.exists(filePath):
        print (fileName+" already exists. 文件已经存在，请指定其他文件夹")
        return
    else:
        if format == 'csv':
        # CSV
            w = csv.writer(open(filePath, "w"))
            for key, val in JSONOBJ:
                w.writerow([key, val])
        
        elif format == 'pickle':
        # Serialized
            pickle.dump(JSONOBJ, open(filePath,'w'))

        elif format == "json":
        # JSON 
            with open(filePath,'w') as f:
                newData = json.dumps(JSONOBJ, sort_keys=True, indent=4)
                f.write(newData)
                f.close()
        else :
            print "Unknown format. 格式不存在" 