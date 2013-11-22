#!/bin/bash

die () {
    echo >&2 "$@"
    exit 1
}

[ "$#" -eq 1 ] || die "1 argument required, $# provided"

# test extension 
if test ${1##*.} != "py"; then die "Invalid file extension. File should be py"; fi

# get current dir for script

# launch script
nosetests --rednose --force-color `/home/clemsos/Dev/mitras/tests`$1