#!/bin/bash

MENTION_COUNT=10000
COMPONENTS="0-1000"
OUTPUT_SIZE=100
STREAM_URL=https://stream.twitter.com/1/statuses/sample.json
CURL_OPTIONS=
MENTIONS=`mktemp -t mentions`
SCRIPT=`mktemp -t script`

function Usage {
    echo Usage: `basename $0` -u username [-p password] [-n num] [-s size] [-q] [-v] [-o]
    exit 1
}

function Dependencies {
    echo `basename $0` requires that Graphviz and Python be installed and on your PATH
    exit 2
}

test `which python` || Dependencies
test `which sfdp` || Dependencies

while getopts ":n:u:p:s:qvo" opt; do
    case $opt in
        n)
            MENTION_COUNT=$OPTARG
            ;;
        o)
            OPEN=yes
            ;;
        u)
            TWITTER_USERNAME=$OPTARG
            ;;
        p)
            TWITTER_PASSWORD=$OPTARG
            ;;
        q)
            QUIET=yes
            ;;
        s)
            OUTPUT_SIZE=$OPTARG
            ;;
        v)
            PROGRESS=-v
            ;;
        \?)
            Usage
            ;;
        :)
            Usage
            ;;
    esac
done

if [ "${TWITTER_USERNAME}" == "" ]; then Usage; fi

if [ "${TWITTER_PASSWORD}" == "" ]; then
    stty -echo
    read -p "Twitter password:" TWITTER_PASSWORD; echo
    stty echo
fi

test $QUIET || echo Collecting ~${MENTION_COUNT} mentions from ${STREAM_URL} at ${MENTIONS}

cat > ${SCRIPT} <<EOF
import os
import sys
import json
import time
import base64
import urllib2
from optparse import OptionParser

parser = OptionParser()
parser.add_option('-u', action='store', dest='username')
parser.add_option('-p', action='store', dest='password')
parser.add_option('-n', action='store', dest='target', default=1000, type=int)
parser.add_option('-v', action='store_true', dest='verbose', default=False)
(options, args) = parser.parse_args()

request = urllib2.Request("https://stream.twitter.com/1/statuses/sample.json")
request.add_header("Authorization", "Basic %s" % base64.encodestring('%s:%s' % (options.username, options.password)).replace('\n',''))
stream = urllib2.urlopen(request)

count=0
start=time.time()

for line in stream:
    if len(line) == 0:
        continue
        
    message = json.loads(line)
    if (message.get("entities") == None):
        continue
    user = message["user"]["screen_name"]
    for mentionee in message.get("entities").get("user_mentions"):
        print "\"%s\" -> \"%s\"" % (user.lower(), mentionee["screen_name"].lower())
        count += 1
        if (options.verbose) and (time.time() - start > 5):
            start = time.time()
            print >> sys.stderr, "\r%s mentions collected" % count,
    if (count > options.target):
        print >> sys.stderr, "\r%s mentions collected" % count
        break
EOF

python -u ${SCRIPT} -u ${TWITTER_USERNAME} -p ${TWITTER_PASSWORD} -n ${MENTION_COUNT} ${PROGRESS} > ${MENTIONS}

test $QUIET || echo Done collecting mentions

test $QUIET || echo Rendering graph

sort ${MENTIONS} \
    | uniq \
    | cat <(echo "digraph mentions {") - <(echo "}") \
    | ccomps -zX#${COMPONENTS} \
    | grep "-" \
    | cat <(echo "digraph mentions {") - <(echo "}") \
    | tee $0.gv \
    | sfdp \
        -Gbgcolor=black \
        -Ncolor=white \
        -Ecolor=white \
        -Nwidth=0.02 \
        -Nheight=0.02 \
        -Nfixedsize=true \
        -Nlabel='' \
        -Earrowsize=0.4 \
        -Gsize=${OUTPUT_SIZE} \
        -Gratio=fill \
    | neato -s -n2 -Nlabel='' -Tpng \
    > $0.png
    
test $OPEN && open $0.png

test $QUIET || echo Done

rm ${SCRIPT}