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


python `dirname ${CUR}`/compute_protomemes.py 