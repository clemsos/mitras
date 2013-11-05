#!/bin/bash
die () {
    echo >&2 "$@"
    exit 1
}

[ "$#" -eq 1 ] || die "1 argument required, $# provided"

db=$1

read -p "Delete '${db}' database (y/n)?" choice
case "$choice" in 
  y|Y ) mongo ${db} --eval "db.dropDatabase()";;
  n|N ) echo "Nothing happened";;
  * ) echo "invalid input";;
esac


