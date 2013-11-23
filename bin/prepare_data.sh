#!/bin/bash

die () {
    echo >&2 "$@"
    exit 1
}

# get current dir for script
CUR="${BASH_SOURCE[0]}";
if([ -h "${CUR}" ]) then
  while([ -h "${CUR}" ]) do CUR=`readlink -m "${CUR}"`; done
fi
pushd . > /dev/null
cd `dirname ${CUR}` > /dev/null
CUR=`pwd`;
popd  > /dev/null


# define directory containing CSV files
_csv_directory="`dirname ${CUR}`/data/datazip"

# go into directory
cd $_csv_directory

# get a list of CSV files in directory
_csv_files=`ls -1 week*.csv`


# loop through csv files
for _csv_file in ${_csv_files[@]}
do

    python `dirname ${CUR}`/prepare.py $_csv_file

done
exit

# find  data/datazip/ -name week*.csv
# test extension 
# if test ${1##*.} != "csv"; then die "Invalid file extension. File should be .csv"; fi

# launch script