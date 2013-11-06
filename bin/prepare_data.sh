#!/bin/bash

die () {
    echo >&2 "$@"
    exit 1
}

[ "$#" -eq 1 ] || die "1 argument required, $# provided"

# test extension 
if test ${1##*.} != "csv"; then die "Invalid file extension. File should be csv"; fi

# get current dir for script
CUR="${BASH_SOURCE[0]}";
if([ -h "${CUR}" ]) then
  while([ -h "${CUR}" ]) do CUR=`readlink -m "${CUR}"`; done
fi
pushd . > /dev/null
cd `dirname ${CUR}` > /dev/null
CUR=`pwd`;
popd  > /dev/null

# launch script
python `dirname ${CUR}`/prepare.py $1