#!/bin/bash

# show commands being executed, per debug
set -x

# define database connectivity
_db="test"
_db_user="miner"
_db_password="WmQNV465pWcqq8K8"

# define directory containing CSV files
_csv_directory="/home/clemsos/Dev/mitras/data"

# go into directory
cd $_csv_directory

# get a list of CSV files in directory
_csv_files=`ls -1 *.csv`

# loop through csv files
for _csv_file in ${_csv_files[@]}
do
	# remove file extension
  	_csv_file_extensionless=`echo $_csv_file | sed 's/\(.*\)\..*/\1/'`

  	# define table name
  	_table_name="${_csv_file_extensionless}"

  	# add quote marks to header
  	sed -i -r '1{s/(^|$)/"/g;s/,/","/g}' $_csv_file

  	# get header columns from CSV file
  	_header_columns=`head -1 $_csv_directory/$_csv_file | sed s'/.$//' | tr ',' '\n' | sed 's/^"//' | sed 's/"$//' | sed 's/ /_/g'`
  	_header_columns_string=`head -1 $_csv_directory/$_csv_file | sed s'/.$//' | sed 's/ /_/g' | sed 's/"//g'`

   # ensure table exists
	mysql -u $_db_user -p$_db_password $_db << eof
	    CREATE TABLE IF NOT EXISTS \`$_table_name\` (
	      id int(11) NOT NULL auto_increment,
	      PRIMARY KEY  (id)
	    ) ENGINE=MyISAM DEFAULT CHARSET=utf8
eof

	# loop through header columns
	for _header in ${_header_columns[@]}
	do
		# add column
    	mysql -u $_db_user -p$_db_password $_db --execute="alter table \`$_table_name\` add column \`$_header\` text"
	done

	# import csv into mysql
  	mysqlimport --ignore-lines=1 --fields-terminated-by=',' --lines-terminated-by="\n" --columns=$_header_columns_string -u $_db_user -p$_db_password $_db $_csv_directory/$_csv_file   

  	# fix 
	# mysql -u $_db_user -p$_db_password $_db --execute="delete from \`$_table_name\` WHERE mid = 'mid'"

done

exit