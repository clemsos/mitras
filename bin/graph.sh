#!/bin/bash

die () {
    echo >&2 "$@"
    exit 1
}


[ "$#" -eq 1 ] || die "1 argument required (python script name), $# provided" 

# /home/clemsos/Dev/mitras/data/out/tmph6J4PY.gv
gv_file=$1
echo $gv_file

sfdp -Gbgcolor=black -Ncolor=white -Ecolor=white -Nwidth=0.05  -Nheight=0.05 -Nfixedsize=true -Nlabel='' -Earrowsize=0.4     -Gsize=75 -Gratio=fill -Tpng $gv_file > test2.png 
