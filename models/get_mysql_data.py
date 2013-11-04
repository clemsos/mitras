#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb

nbRecords=str(3000)

# connect to Mysql
sql_db = MySQLdb.connect(host="localhost", user="miner", passwd="WmQNV465pWcqq8K8", db="test")
sql_db.set_character_set('utf8')

# get some data
cursor = sql_db.cursor()
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')

# execute SQL select statement
statement="SELECT * FROM  `sampleweibo` LIMIT 0 ," +nbRecords
cursor.execute(statement)

# get the result data
db.commit()
dataset = int(cursor.rowcount)