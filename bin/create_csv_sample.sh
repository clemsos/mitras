#!/bin/bash
die () {
    echo >&2 "$@"
    exit 1
}

[ "$#" -eq 1 ] || die "1 argument required, $# provided"

f=/home/clemsos/Dev/mitras/data/datazip/others/userdata.csv

echo "Creating a sample from ${f} of ${1} lines "
head -n${1} ${f} > sampleweibo.csv