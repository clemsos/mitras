#!/bin/bash

die () {
    echo
    echo >&2 "$@"
    help
    exit 1
}

help () {
    echo """
    Export a dataset from specific in mongo record to csv
    
    usage : 
    meme2csv.sh <meme name>
        <meme name> : exact name in the db
    """
}

[ "$#" -eq 1 ] || die "    ERROR : 1 argument required (meme name), $# provided" 

meme_name=$1

# get current dir for script
CUR="${BASH_SOURCE[0]}";
if([ -h "${CUR}" ]) then
  while([ -h "${CUR}" ]) do CUR=`readlink -m "${CUR}"`; done
fi
pushd . > /dev/null
cd `dirname ${CUR}` > /dev/null
CUR=`pwd`;
popd  > /dev/null

file_path=$CUR/out/meme.csv
echo "exporting data from " $meme_name "to " $file_path

mongoexport --host localhost --db weibodata --collection memes --csv --fields name,tweets -q '{"name":"'${meme_name}'" }' --out $file_path