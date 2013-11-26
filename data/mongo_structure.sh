#!/bin/bash

die () {
    echo >&2 "$@"
    exit 1
}

help () {
    echo " mongo_structure.sh 'collection' "
}

[ "$#" -eq 1 ] || die "1 argument required (collection name), $# provided" 

collection=$1

db=$1
 mongo weibodata --eval "var collection = '${collection}'" utils/variety.js
