#!/bin/bash

die () {
    echo >&2 "$@"
    exit 1
}


[ "$#" -eq 1 ] || die "1 argument required (python script name), $# provided" 

script=$1

kill -9 $(ps aux | grep 'python `${script}` | awk '{print $2}')
# kill -9  $(ps aux | grep 'python ${script}'| awk '{print $2}')


# kill -9  $(ps aux | grep 'python compute_protomemes.py'| awk '{print $2}')